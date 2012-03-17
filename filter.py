import networkx as nx
import matplotlib.pyplot as plt
from socket import socket as sock, AF_INET, SOCK_DGRAM 
from select import select

POLL = 0
READ_SIZE = 4096

class Filter: 
   g = nx.Graph()


   def __init__(self, host="", port=6969):
      self.host = host
      self.port = port
      
   def addFlowToGraph(routerSrc, dst, nextHop):
      if nextHop == "0.0.0.0":
         flowGraph.add_edge(routerSrc, dst)
      else:
         flowGraph.add_edge(routerSrc, nextHop)
      
   def updateNetworkGraph():
      pos=nx.spring_layout(flowGraph)
      nx.draw(flowGraph, pos, fontsize=10)
      plt.axis('off')
      plt.savefig("graph.png")
  

   def updateMetrics(self, unique, record): 
      #Check if the flow record is already in the dictionary
      if unique in self.data:
         flowRecord = self.data[unique]
         # Check if start times are the same
         if flowRecord[START] == record[START]:
            self.data[unique][L3_BYTES] += record[L3_BYTES]
            self.data[unique][END] = record[END]
            
         




   def __init__(self, host="", port=6969):
      self.host = host
      self.port = port
      self.listener = sock(AF_INET, SOCK_DGRAM, 0)
      self.listener.bind((host, port))
      self.flowGraph = nx.Graph()
      self.data = {}
      self.nodeNames = ["---"]
      self.nodeData = ["Select a node."]
      self.avgByteGraph = []
      self.avgLenGraph = []
      self.numFlowsGraph = []
      self.buffer = ""
      self.lastTwentyRecords = []
      self.lastTwentyHeaders = []
                
   def updateNetworkGraph(self):
      pos=nx.spring_layout(self.flowGraph)
      nx.draw(self.flowGraph, pos, fontsize=10)
      plt.axis('off')
      plt.savefig("graph.png")
  
   def addFlowToGraph(self, routerSrc, dst, nextHop):
      if nextHop == "0.0.0.0":
         self.flowGraph.add_edge(routerSrc, dst)
      else:
         self.flowGraph.add_edge(routerSrc, nextHop)

   def getAvgBytes(self):
      
      
   def getAvgFlowLength(self):
      
   
   def getNumOfFlows(self):
      return self.numFlowsGraph   

   def generateGraphs(self):
      return [ self.getAvgBytes(), self.getAvgFlowLength(), self.getNumOfFlows() ]

   def update(self, nodeIndex):
      while select([self.listener], [], [], POLL)[0]:
         self.buffer += self.listener.recv(READ_SIZE)
      
      while self.buffer != "":
        self.buffer[:HDR_LEN]         
         
         
      return [ self.generateGraphs(), self.getNewNodes(), self.nodeData[nodeIndex] ]
       
   def updateMetrics(self, unique, record): 
    #Check if the flow record is already in the dictionary
      if unique in self.data:
         flowRecord = self.data[unique]
         # Check if start times are the same
         if flowRecord[START] == record[START]:
            self.data[unique][L3_BYTES] += record[L3_BYTES]
            self.data[unique][END] = record[END]
      else: 
         self.data[unique] = record      
     
     
