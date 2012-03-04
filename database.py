
class Database:
  def __init__(self, fwdAddr=None):
    self.data = {"R": {}, "H":{}}
    self.numHdrs = 0
  
  def insert(self, table, key=None, data):
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

  def get(self, table, key):
    if table == "H":
      return self.data[table][key] 
    elif table == "R":
      return self.data[table][key]
    else:
      return None   

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

