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
  
    protocolName = protocols[portNum]
  except KeyError:
    protocolName = str(portNum)
  
  return protocolName

# DEBUG (DUMP HEADER)
def dumpHeader(pktData):
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
def dumpRecord(pktData):
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

def formatIP(ipAddr):
  oct1 = (ipAddr & 0xFF000000) >> 24
  oct2 = (ipAddr & 0x00FF0000) >> 16
  oct3 = (ipAddr & 0x0000FF00) >> 8
  oct4 = (ipAddr & 0x000000FF)
  return str(oct1)+"."+str(oct2)+"."+str(oct3)+"."+str(oct4)

