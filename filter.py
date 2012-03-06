#!/usr/bin/env python

import random

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

    def update(self):
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
        if (random.random() > 0.9):
            return self.graphs, True
        else:
            return self.graphs, False

    def checkNetGraph(self):
        if (random.random() > 0.9):
            self.modifyImage()
            return True
        else:
            return False

    def modifyImage(self):
        self.im = self.im.rotate(1)
        self.im.save(self.graphFile)
