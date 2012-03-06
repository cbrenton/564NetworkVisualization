import networkx as nx
import matplotlib.pyplot as plt
from socket import socket as sock, AF_INET, SOCK_DGRAM
from select import select

flowGraph = nx.Graph()


def addFlowToGraph(routerSrc, dst, nextHop):
   if nextHop == "0.0.0.0":
      flowGraph.add_edge(routerSrc, dst)
   else:
      flowGraph.add_edge(routerSrc, nextHop)
      
def updateNetworkGraph():
   pos=nx.spring_layout(flowGraph)
   nx.draw(flowGraph, pos)
   #plt.axis('off')
   plt.savefig("graph.png")
      
addFlowToGraph("3.3.3.3", "1.1.1.1", "5.5.5.5")  
addFlowToGraph("1.1.1.1", "2.2.2.2", "3.3.3.3")
addFlowToGraph("3.3.3.3", "1.1.1.1", "4.4.4.4")
addFlowToGraph("3.3.3.3", "5.5.5.5", "0.0.0.0")
addFlowToGraph("1.1.1.1", "7.7.7.7", "0.0.0.0")
addFlowToGraph("1.1.1.1", "6.6.6.6", "0.0.0.0")
updateNetworkGraph()      
      
