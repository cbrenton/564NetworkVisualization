import netflow
import sys

if len(sys.argv) != 2:
  print "Usage: python "+sys.argv[0]+" <netflowcapturefile>"
  exit()

data = open(sys.argv[1], "rb").read()
cl = netflow.Collector()
cl.buffer = data
cl.parseNetFlowPackets() 
