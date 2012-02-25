from struct import pack, pack_into, unpack
import socket 
from array import array as arr

def IPtoBinary(addr):
  return unpack("!L", socket.inet_aton(addr))[0]

version = 5
numFlows = int(raw_input("Enter number of flows: "))
uptime = int(raw_input("Enter device uptime (millis): "))
epochMillis = int(raw_input("Enter system clock in millis (since Epoch): "))
epochNano = int(raw_input("Residual nanoseconds (since Epoch): "))
totalFlowsSeen = int(raw_input("Total flows seen since boot: "))
engineType = int(raw_input("Engine type: "))
engineID = int(raw_input("Engine ID: "))
samplingInterval = int(raw_input("Sampling Interval: "))

pktPayload = arr("c", (24 + (numFlows * 48)) * "\0")

pack_into("!HHLLLLBBH", pktPayload, 0, version, numFlows, uptime, epochMillis, epochNano, totalFlowsSeen, engineType, engineID, samplingInterval)

offset = 24
  
for i in range(numFlows):
  print "=== Flow #"+str(i+1)+" ===" 
  srcIP = IPtoBinary(raw_input("Source IP: "))
  dstIP = IPtoBinary(raw_input("Destination IP: "))
  nextIP = IPtoBinary(raw_input("IP of next hop: "))
  ifIn = int(raw_input("SNMP Input Index: "))
  ifOut = int(raw_input("SNMP Output Index: "))
  numPkts = int(raw_input("Number of Packets in Flow: "))
  l3bytes = int(raw_input("Total Layer 3 Bytes: "))
  flowStart = int(raw_input("Flow Start Time: "))
  flowEnd = int(raw_input("Flow End Time: "))
  srcPort = int(raw_input("Source Port: "))
  dstPort = int(raw_input("Destination Port: "))
  tcpFlags = int(raw_input("TCP Flags: "))
  ipProt = int(raw_input("IP Protocol Type: "))
  tos = int(raw_input("Type of Service (ToS): "))
  srcAS = int(raw_input("Source AS: "))
  dstAS = int(raw_input("Destination AS: "))
  srcNM = int(raw_input("Source Netmask (CIDR): "))
  dstNM = int(raw_input("Destination Netmask (CIDR): "))  

  pack_into("!LLLHHLLLLHHBBBBHHBBH", pktPayload, offset, srcIP, dstIP, nextIP,\
   ifIn, ifOut, numPkts, l3bytes, flowStart, flowEnd, srcPort, dstPort, 0, tcpFlags, ipProt,\
   tos, srcAS, dstAS, srcNM, dstNM, 0)
  offset += 48

fileName = open(raw_input("Output File: "), "wb")
fileName.write(pktPayload)
fileName.close()
