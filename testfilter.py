#!/usr/bin/env python

import random
import string

import visgraph

try:
    from PIL.Image import open
except ImportError, err:
    from Image import open

class TestFilter():
    def __init__(self, length=4):
        self.length = length
        self.graphs = []
        for i in range(length - 1):
            self.graphs.append(visgraph.Graph())
        multi = visgraph.MultiGraph()
        for i in range(3):
            multi.addGraph(visgraph.Graph())
        self.graphs.append(multi)
        
        self.graphFile = "graph.png"
        
        # Open graph.png.
        self.im = open(self.graphFile)

        self.nodes = ["---"]
        self.nodeData = ["Select a node."]
        self.nodeCount = 0

    def update(self, nodeIndex):
        for g in self.graphs:
            try:
                for i in range(g.size):
                    g.data[i] += random.random() / 4.0 - 0.125
                    g.data[i] = min(1.0, max(0.0, g.data[i]))
            except:
                for i in range(len(g.sets)):
                    for j in range(g.sets[i].size):
                        g.sets[i].data[j] += random.random() / 4.0 - 0.125
                        g.sets[i].data[j] = min(1.0, max(0.0, g.sets[i].data[j]))
        updateNetwork = self.checkNetGraph()
        self.newnodes = []
        # Randomly add new nodes.
        while (random.random() < 0.3):
            self.nodes.append(str(self.nodeCount))
            self.newnodes.append(str(self.nodeCount))
            self.nodeCount = self.nodeCount + 1
            self.nodeData.append(''.join(random.choice(string.ascii_uppercase + \
                                                       string.ascii_lowercase + \
                                                       " ") for x in range(random.randint(40,500))))
        return self.graphs, self.newnodes, self.nodeData[nodeIndex]

    def updateRaw(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + " ") for x in range(random.randint(40,5000)))

    def checkNetGraph(self):
        if (random.random() > 0.9):
            self.modifyImage()
            return True
        else:
            return False

    def modifyImage(self):
        self.im = self.im.rotate(1)
        self.im.save(self.graphFile)
