import networkx as nx
import matplotlib.pyplot as plt

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
            
         





