#!/usr/bin/env python

import random
import string

import visgraph

try:
    from PIL.Image import open
    import PIL.ImageOps
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
        self.allNodes = [' ']
        self.allNodeData = ["Select a node."]
        
        self.graphFile = "graph.png"
        
        # Open graph.png.
        self.im = open(self.graphFile)

    def update(self, currentNode):
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
        nodes = []
        while (random.random() < 0.1):
            # Assign a random node label.
            nodes.append(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(3)))
            # Add the new nodes to the list of all nodes.
            self.allNodes.append(nodes[-1])
            # Add random node data.
            self.allNodeData.append(''.join(random.choice(string.ascii_uppercase + string.digits + ' ' + '\n') for x in range(random.randint(3, 700))))
        if (random.random() > 0.9):
            return self.graphs, nodes, self.allNodeData[currentNode], updateNetwork
        else:
            return self.graphs, nodes, self.allNodeData[currentNode], updateNetwork

    def checkNetGraph(self):
        if (random.random() > 0.8):
            self.modifyImage()
            return True
        else:
            return False

    # For debugging purposes only. Modifies graph.png to demonstrate that it is
    # being reloaded.
    def modifyImage(self):
        #self.im = self.im.rotate(1)
        self.im = PIL.ImageOps.invert(self.im)
        #inverted = PIL.ImageOps.invert(self.im)
        #inverted.save("invert.png")
        self.im.save(self.graphFile)
