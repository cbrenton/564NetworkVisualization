from socket import socket as sock, AF_INET, SOCK_DGRAM
from socket import ntohl, ntohs
from select import select
from struct import unpack
import time

# Configuration Parameters 
DATA_READ = 1024
POLL = 0
HDR_LEN = 24
DATA_LEN = 48

# HEADER INDEX CONSTANTS
VERSION = 0
NUM_FLOWS = 1
UPTIME = 2
EPOCH_MS = 3
EPOCH_NS = 4
TOTAL_FLOWS = 5
ENGINE_TYPE = 6
ENGINE_ID = 7
SAMPLE_RATE = 8

# RECORD INDEX CONSTANTS
SRC_IP = 0
DST_IP = 1
HOP_IP = 2
IF_IN = 3
IF_OUT = 4
NUM_PKTS = 5
L3_BYTES = 6
START = 7
END = 8
SRC_PORT = 9
DST_PORT = 10
TCP_FLAGS = 12
IP_PROT = 13
SRV_TYPE = 14
SRC_AS = 15
DST_AS = 16
SRC_MASK = 17
DST_MASK = 18

# Take a single byte containing TCP flags ORed together, 
# and extract the flag names from the byte.\
# Returns the flags separated by spaces 
def expandTCPFlags(flagSummary):
  flags = ["CWR", "ECE", "URG", "ACK", "PSH", "RST", "SYN", "FIN"]
  flagsPresent = []
  bits = bin(flagSummary)[2:].zfill(8)

  for i in range(len(flags)):
    if bits[i] == "1":
      flagsPresent.append(flags[i])

  return " ".join(flagsPresent)

# 
def getIPType(typeNum):
  protocols = {0x00 : "IPv6 Hop-by-Hop Option",
    0x01 : "ICMP",
    0x02 : "IGMP",
   	0x03 : "GGP",
    0x04 : "IP", 
    0x05 : "ST", 
    0x06 : "TCP", 
    0x07 : "CBT",
    0x08 : "EGP",
    0x09 : "IGP",
    0x0A : "BBN-RCC-MON", 
    0x0B : "NVP-II",
    0x0C : "PUP",
    0x0D : "ARGUS",
    0x0E : "EMCON",
    0x0F : "XNET",
    0x10 : "CHAOS",
    0x11 : "UDP",
    0x12 : "MUX",
    0x13 : "DCN-MEAS",
    0x14 : "HMP",
    0x15 : "PRM", 
    0x16 : "XNS-IDP",
    0x17 : "TRUNK-1",
    0x18 : "TRUNK-2",
    0x19 : "LEAF-1",
    0x1A : "LEAF-2",
    0x1B : "RDP", 
    0x1C : "IRTP",
    0x1D : "ISO-TP4",
    0x1E : "NETBLT",
    0x1F : "MFE-NSP",
    0x20 : "MERIT-INP",
    0x21 : "DCCP",  
    0x22 : "3PC",
    0x23 : "IDPR",
    0x24 : "XTP"}
  try:
    protName = protocols[typeNum]
  except KeyError:
    protName = "Other ("+str(typeNum)+")"
  return protName

def translateWellKnownPort(portNum):
  protocols = {21 : "FTP", 
   22 : "SSH", 
   23 : "Telnet",
   25 : "SMTP",
   37 : "Time", 
   43 : "WhoIs", 
   53 : "DNS", 
   69 : "TFTP", 
   80 : "HTTP",
   115 : "SFTP", 
   118 : "SQL Services",
   119 : "NNTP",
   123 : "NTP (Network Time Protocol)",
   156 : "SQL Service",
   161 : "SNMP", 
   179 : "BGP", 
   194 : "IRC",
   443 : "HTTP over TLS/SSL",
   989 : "FTP data over TLS/SSL",
   990 : "FTP control over TLS/SSL", 
   993 : "IMAP4 over TLS/SSL",
   995 : "POP3 over TLS/SSL"} 
  
  try: 
    protocolName = protocols[portNum]
  except KeyError:
    protocolName = str(portNum)
  
  return protocolName


def formatIP(ipAddr):
  oct1 = (ipAddr & 0xFF000000) >> 24
  oct2 = (ipAddr & 0x00FF0000) >> 16
  oct3 = (ipAddr & 0x0000FF00) >> 8
  oct4 = (ipAddr & 0x000000FF)
  return str(oct1)+"."+str(oct2)+"."+str(oct3)+"."+str(oct4)

class Collector:
  def __init__(self, db=Database(), host="", port=9996):
    self.listener = sock(AF_INET, SOCK_DGRAM, 0)
    self.listener.bind((host, port))
    self.buffer = ""
    self.database = db
    self.pktLogBin = open("netflowlogBin.txt", "wb")
    self.pktLog = open("netflowlog.txt", "w")
  
  # "Main" Method to collect and store data
  def collectNetFlowPackets(self):
    if self.getData():
      print "Flow Received!"
      self.parseNetFlowPackets() 
   
  # Close the socket 
  def cleanup(self):
    self.listener.close()
 
  # Check for data and gather it
  def getData(self):
    isData = False
    while select([self.listener], [], [], POLL)[0]:
      data = self.listener.recv(DATA_READ) 
      self.buffer += data
      print "Received: \n"+repr(data)+"\nSize: "+str(len(data))
      self.pktLog.write(repr(data))
      self.pktLogBin.write(data)
      isData = True
    return isData

  # Parse the NetFlow V5 header and any associated flows
  def parseNetFlowPackets(self):
    hdrData = self.parseNetFlowHeader(self.buffer[:HDR_LEN])
    idx = HDR_LEN
    numFlows = hdrData[NUM_FLOWS]
    while numFlows > 0:
      self.parseNetFlowRecord(self.buffer[idx:idx+DATA_LEN])
      numFlows -= 1
      idx += DATA_LEN

  # Header Format (24 bytes)
  # 0                         16                 32 bits
  # |    NetFlow Version      |     Flow Count    | 
  # |              Device Uptime                  | 
  # |          milliseconds since Epoch           |
  # |         residual nanosec from above         |  
  # |               total flows seen              |
  # | engine type | engine ID | sampling interval | 
  # @param pktData packet data as a string 
  def parseNetFlowHeader(self, pktData):
    pktPayload = list(unpack("!HHLLLLBBH", pktData))
    self.dumpHeader(pktPayload)
    self.storeHeader(pktPayload, time.time())
    return pktPayload

  # DEBUG (DUMP HEADER)
  def dumpHeader(self, pktData):
    print "==== NetFlow Header Dump ===="
    print "NetFlow Version: "+str(pktData[VERSION])
    print "Number of Flows in this Export: "+str(pktData[NUM_FLOWS])
    print "System Uptime in Milliseconds: "+str(pktData[UPTIME])
    print "Time since Epoch in Milliseconds: "+str(pktData[EPOCH_MS])
    print "Residual Nanoseconds from Above: "+str(pktData[EPOCH_NS])
    print "Total Number of Flows Since Boot: "+str(pktData[TOTAL_FLOWS])
    print "Engine Type: "+str(pktData[ENGINE_TYPE])
    print "Engine ID: "+str(pktData[ENGINE_ID])
    print "Sampling Interval: "+str(pktData[SAMPLE_RATE])
  
  # DEBUG (DUMP RECORD)
  def dumpRecord(self, pktData):
    srcIP = formatIP(pktData[SRC_IP])
    dstIP = formatIP(pktData[DST_IP])
    nextHop = formatIP(pktData[HOP_IP])
    snmpIn = pktData[IF_IN]
    snmpOut = pktData[IF_OUT]
    numPkts = pktData[NUM_PKTS]
    L3Bytes = pktData[L3_BYTES]
    flowStart = pktData[START]
    flowEnd = pktData[END]
    srcPort = pktData[SRC_PORT]
    dstPort = pktData[DST_PORT]
    tcpFlags = pktData[TCP_FLAGS]
    ipProt = pktData[IP_PROT]
    tos = pktData[SRV_TYPE]
    srcAS = pktData[SRC_AS]
    dstAS = pktData[DST_AS]
    srcMask = pktData[SRC_MASK]
    dstMask = pktData[DST_MASK]

    print "==== NetFlow Record Dump ===="
    print "Source: "+srcIP
    print "Destination: "+dstIP
    print "Next Hop: "+nextHop
    print "SNMP Input Interface: "+str(snmpIn)
    print "SNMP Output Interface: "+str(snmpOut)
    print "Number of Packets in Flow: "+str(numPkts)
    print "Total Layer 3 Bytes in Flow: "+str(L3Bytes)
    print "Flow started at system boot +"+str(flowStart/1000)+" seconds"
    print "Flow last observed at system boot +"+str(flowEnd/1000)+" seconds"
    print "Flow has been alive for "+str((flowEnd/1000)-(flowStart/1000))+" seconds"
    print "UDP/TCP Source Port: "+translateWellKnownPort(srcPort)
    print "UDP/TCP Destination Port: "+translateWellKnownPort(dstPort)
    print "Cumulative TCP Flags: "+expandTCPFlags(tcpFlags)
    print "IP Protocol Type: "+getIPType(ipProt)
    print "Type of Service: "+str(tos)
    print "Source Autonomous System Number: "+str(srcAS)
    print "Destination Autonomous System Number: "+str(dstAS)
    print "Source Netmask: /"+str(srcMask)
    print "Destination Netmask: /"+str(dstMask)   
  
  # Record format: 
  # http://netflow.caligare.com/netflow_v5.htm
  def parseNetFlowRecord(self, pktData):
    pktPayload = list(unpack("!LLLHHLLLLHHBBBBHHBBH", pktData))
    self.dumpRecord(pktPayload) 
    self.storeRecord(pktPayload[:2], pktPayload[2:])
    return pktPayload

  # Stores flows by src and dest
  def storeRecord(self, key, record):
    self.db.insert("R", key, record)
  
  # Stores headers by order received 
  def storeHeader(self, key, header):  
    self.db.insert("H", key, record)

if __name__ == "__main__":
  flowCollector = Collector()
  data = Database()
  #try: 
  while True:
    flowCollector.collectNetFlowPackets()
 # except Exception: 
  # "Error!\nWriting raw packets to log!"
   # flowCollector.pktLog.close()
   # exit()
