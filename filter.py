from select import select
from socket import socket as sock, AF_INET, SOCK_DGRAM
from struct import unpack

DATA_READ = 4096

# FILTER PKT FORMAT
TYPE = 0

# FILTER PKT CONSTANTS
FULL_RECORD = 0

class Filter: 

  def __init__(self, host="", port=6969):
    self.listener = sock(AF_INET, SOCK_DGRAM, 0)
    self.listener.bind((host, port))
    
  def getNetInfo():
    buff = ""
    while select([self.listener], [], [], POLL)[0]:
      (collectorIP, data) = self.listener.recvfrom(DATA_READ)
      buff += data
    self.processNetInfo(buff)

  def processNetInfo(data):
    while data != "":
      if unpack("!B", data[0])[0] == FULL_RECORD:
        unpack("!LLLLL", data[1:])        


    #numPkts = pktData[NUM_PKTS]
    #L3Bytes = pktData[L3_BYTES]
    #flowStart = pktData[START]
    #flowEnd = pktData[END]
    #srcPort = pktData[SRC_PORT]
    #dstPort = pktData[DST_PORT]
    #tcpFlags = pktData[TCP_FLAGS]
    #ipProt = pktData[IP_PROT]
    #tos = pktData[SRV_TYPE]
    #srcAS = pktData[SRC_AS]
    #dstAS = pktData[DST_AS]
    #srcMask = pktData[SRC_MASK]
    #dstMask = pktData[DST_MASK]  
 
     
            
            

