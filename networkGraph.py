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
   nx.draw(flowGraph, pos, fontsize=10)
   plt.axis('off')
   plt.savefig("graph.png")
      
addFlowToGraph("10.4.11.1", "10.4.11.100", "0.0.0.0")
addFlowToGraph("10.4.11.1", "10.4.11.101", "0.0.0.0")
addFlowToGraph("10.4.11.1", "Collector", "0.0.0.0")

addFlowToGraph("10.4.11.2", "10.4.11.200", "0.0.0.0")
addFlowToGraph("10.4.11.2", "10.4.11.202", "0.0.0.0")
addFlowToGraph("10.4.11.2", "Collector", "0.0.0.0")

addFlowToGraph("10.4.11.3", "10.4.11.50", "0.0.0.0")
addFlowToGraph("10.4.11.3", "10.4.11.51", "0.0.0.0")
addFlowToGraph("10.4.11.3", "Collector", "0.0.0.0")

addFlowToGraph("10.4.11.4", "10.4.11.150", "0.0.0.0")
addFlowToGraph("10.4.11.4", "10.4.11.151", "0.0.0.0")
addFlowToGraph("10.4.11.4", "Collector", "0.0.0.0")

addFlowToGraph("10.4.11.2", "10.4.11.4", "10.4.11.4")
addFlowToGraph("10.4.11.4", "10.4.11.3", "10.4.11.3")
addFlowToGraph("10.4.11.3", "10.4.11.1", "10.4.11.1")
addFlowToGraph("10.4.11.1", "10.4.11.2", "10.4.11.2")


updateNetworkGraph()      
      
