from socket import socket as sock, AF_INET, SOCK_DGRAM
from socket import ntohl, ntohs
from select import select
from struct import unpack
from database import Database
from nfutil import *
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

class Collector:
  def __init__(self, db=Database(), host="", port=9996,\
   dstHost="", dstPort=6969, playback=False, logIt=True):
    self.listener = sock(AF_INET, SOCK_DGRAM, 0)
    self.listener.bind((host, port))
    self.sender = sock(AF_INET, SOCK_DGRAM, 0)
    self.dstHost = dstHost
    self.dstPort = dstPort
    self.buffer = ""
    self.database = db
    self.logIt = logIt
    self.playback = playback
    self.pktLogBin = open("../exports/" + math.ceil(time()) + ".ngl", "wb")
  
  # "Main" Method to collect and store data
  def collectNetFlowPackets(self):
    if self.playback:
       print "Playing Back From Logs!"
       self.playBack()
    elif self.getData():
      print "Flow Received!"
      self.parseNetFlowPackets() 
   
  # Close the socket 
  def cleanup(self):
    self.listener.close()
 

  def playBack(self):
    path = os.path.abspath("exports")
    logsPathTuple = os.walk(path)
    for logfile in logsPathTuple[2]:
       if logfile[-4:] == ".ngl":
          inFile = open("../exports/" + logfile, "rb")
          self.buffer = inFile.read()
          while len(buffer) != 0 :
            numberOfFlows = int(self.buffer[4:7]) endIndex = 24 + 52 * numberOfFlows self.sender.sendto(buffer[:endIndex], (dstHost, dstPort))
            buffer = buffer[endIndex:]
          inFile.close()
       

  # Check for data and gather it
  def getData(self):
    while select([self.listener], [], [], POLL)[0]:
      recvReturn = self.listener.recvfrom(DATA_READ) 
      data = recvReturn[0]
      data = data + pack("!L", recvReturn[1])
      # Pass the NetFlow Record + RouterIP to the filter
      self.sender.sendto(data, (self.dstHost, self.dstPort))
      self.buffer += data
      print "Received: \n"+repr(data)+"\nSize: "+str(len(data))
      if self.logIt:
         slf.pktLogBin.write(sys.getsizeof(data))
         self.pktLogBin.write(data)
    return self.buffer != ""

  # Parse the NetFlow V5 header and any associated flows
  def parseNetFlowPackets(self):
    hdrData = self.parseNetFlowHeader(self.buffer[:HDR_LEN])
    idx = HDR_LEN
    numFlows = hdrData[NUM_FLOWS]
    while numFlows > 0:
      self.parseNetFlowRecord(self.buffer[idx:idx+DATA_LEN])
      numFlows -= 1
      idx += DATA_LEN
    
    self.buffer = self.buffer[:HDR_LEN+(numFlows * DATA_LEN)]

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
    nfutil.dumpHeader(pktPayload)
    self.storeHeader(pktPayload, time.time())
    return pktPayload
 
  # Record format: 
  # http://netflow.caligare.com/netflow_v5.htm
  def parseNetFlowRecord(self, pktData):
    pktPayload = list(unpack("!LLLHHLLLLHHBBBBHHBBH", pktData))
    nfutil.dumpRecord(pktPayload) 
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
