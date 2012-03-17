<<<<<<< HEAD
from socket import socket as sock, AF_INET, SOCK_DGRAM
=======
import time
>>>>>>> 375b9190bf31a70703ab98abc76e182efe9c32bc

class Database:
  def __init__(self, fwdAddr="127.0.0.1". fwdPort=6969, filters=[]):
    self.data = {"R": {}, "H":{}}
    self.numHdrs = 0
    self.sender = sock
    self.filterAddr = fwdAddr
    self.filterPort = fwdPort
    self.filters = filters
  
  def insert(self, table, key=None, data=None):
    if table == "H":
      self.data[table][self.numHdrs] = HeaderInfo(data)
      self.numHdrs += 1
    elif table == "R":
      try:   
        pktInfo = self.data[table][key].update(key, data)
      except KeyError:
        self.data[table][key] = RecordInfo(data)
        pktInfo = RecordInfo(data)
    # Send packet data

  def fwdData(self, data):
    for f in filters:
      data = f.apply(data)
        
     

  def get(self, table, key):
    if table == "H":
      return self.data[table][key] 
    elif table == "R":
      return self.data[table][key]
    else:
      return None   
   
  def close(self):
    f = open('dbDump.txt', 'w')

    f.write("================================\n")
    f.write("=== Header Dump ===\n\n")
    for h in self.data["H"]:
      f.write("Version: " + h.version + '\n')
      f.write("Number of Flows: " + h.numFlows + '\n')
      f.write("Router Uptime: ")
      days = h.uptime / 86400000
      hours = (h.uptime % 86400000) / 3600000
      minutes = (h.uptime % (hours * 3600000)) / 60000
      seconds = (h.uptime % (minutes * 60000)) / 1000
      f.write(days + " days ")
      f.write(hours + " hours ")
      f.write(minutes + " minutes ")
      f.write(seconds + " seconds\n")
      f.write("System Time: " + \
       	time.ctime(h.epocMS / 1000 + h.epocNs / 1000000000 + '\n'))
      f.write("Total Number of Flows: " + h.totalFlows + '\n')
      f.write("Sampling Interval : " + h.samplingInterval + '\n')
      
    f.write("\n\n\n================================\n")
       
    f.write("=== NetFlow Record Dump ===\n")
      
    for pktData in self.data["R"]:
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

      f.write("Source: "+srcIP)
      f.write("\nDestination: "+dstIP)
      f.write("\nNext Hop: "+nextHop)
      f.write("\nSNMP Input Interface: "+str(snmpIn))
      f.write("\nSNMP Output Interface: "+str(snmpOut))
      f.write("\nNumber of Packets in Flow: "+str(numPkts))
      f.write("\nTotal Layer 3 Bytes in Flow: "+str(L3Bytes))
      f.write("\nFlow started at system boot +"+str(flowStart/1000)+" seconds")
      f.write("\nFlow last observed at system boot +"+str(flowEnd/1000)+\
       " seconds")
      f.write("\nFlow has been alive for "+str((flowEnd/1000)-\
       (flowStart/1000))+" seconds")
      f.write("\nUDP/TCP Source Port: "+translateWellKnownPort(srcPort))
      f.write("\nUDP/TCP Destination Port: "+translateWellKnownPort(dstPort))
      f.write("\nCumulative TCP Flags: "+expandTCPFlags(tcpFlags))
      f.write("\nIP Protocol Type: "+getIPType(ipProt))
      f.write("\nType of Service: "+str(tos))
      f.write("\nSource Autonomous System Number: "+str(srcAS))
      f.write("\nDestination Autonomous System Number: "+str(dstAS))
      f.write("\nSource Netmask: /"+str(srcMask))
      f.write("\nDestination Netmask: /"+str(dstMask))  
    f.close()
       




class NetFlowInfo:
  def __init__(self, timestampMs):
    pass

class HeaderInfo(NetFlowInfo):
  def __init__(self, dataGroup):    
    self.version = dataGroup[VERSION]
    self.numFlows = dataGroup[NUM_FLOWS]
    self.uptime = dataGroup[UPTIME]
    self.epochMs = dataGroup[EPOCH_MS]
    self.epochNs = dataGroup[EPOCH_NS]
    self.totalFlows = dataGroup[TOTAL_FLOWS]
    self.engineType = dataGroup[ENGINE_TYPE]
    self.engineID = dataGroup[ENGINE_ID]  
    self.samplingInterval = dataGroup[SAMPLE_RATE]

class RecordInfo(NetFlowInfo):
  def __init__(self, dataGroup): 
    self.srcIP = dataGroup[SRC_IP]
    self.dstIP = dataGroup[DST_IP] 
    self.nextHop = dataGroup[HOP_IP]
    self.snmpIn = dataGroup[IF_IN]
    self.snmpOut = dataGroup[IF_OUT]
    self.numPkts = dataGroup[NUM_PKTS]
    self.L3Bytes = dataGroup[L3_BYTES]
    self.flowStart = dataGroup[START]
    self.flowStop = dataGroup[END]
    self.srcPort = dataGroup[SRC_PORT]
    self.dstPort = dataGroup[DST_PORT]
    self.tcpFlags = dataGroup[TCP_FLAGS]
    self.ipProt = dataGroup[IP_PROT]
    self.tos = dataGroup[SRV_TYPE]
    self.srcAS = dataGroup[SRC_AS]
    self.dstAS = dataGroup[DST_AS] 
    self.srcMask = dataGroup[SRC_MASK]
    self.dstMask = dataGroup[DST_MASK]

  def update(self, key, dataGroup):
    delta = {}

    if self.nextHop != dataGroup[HOP_IP]:
      delta[HOP_IP] = dataGroup[HOP_IP]
    if self.numPkts != dataGroup[NUM_PKTS]:
      delta[NUM_PKTS] = dataGroup[NUM_PKTS]
    if self.L3Bytes != dataGroup[L3_BYTES]:
      delta[L3_BYTES] = dataGroup[L3_BYTES]
    if self.flowStart != dataGroup[START]:
      delta[START] = dataGroup[START]
    if self.flowStop != dataGroup[END]:
      delta[END] = dataGroup[END]
    if self.srcPort != dataGroup[SRC_PORT]:
      delta[SRC_PORT] = dataGroup[SRC_PORT]
    if self.dstPort != dataGroup[DST_PORT]:
      delta[DST_PORT] = dataGroup[DST_PORT]
    if self.tcpFlags != dataGroup[TCP_FLAGS]:
      delta[TCP_FLAGS] = dataGroup[TCP_FLAGS]
    if self.ipProt != dataGroup[IP_PROT]:
      delta[IP_PROT] = dataGroup[IP_PROT]
    if self.tos != dataGroup[SRV_TYPE]:
      delta[SRV_TYPE] = dataGroup[SRV_TYPE]
    
    return delta

