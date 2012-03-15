#!/usr/bin/env python

import random

# The Python OpenGL package can be found at
# http://PyOpenGL.sourceforge.net/
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Graph():
    def __init__(self, size=20, yMin=0.0, yMax=1.0, yStep=0.2, data=None):
        self.size = size
        self.yMin = yMin
        self.yMax = yMax
        self.yRange = self.yMax - self.yMin
        self.yStep = yStep
        self.fg = [0.2, 0.4, 0.4]
        self.bg = [1.0, 1.0, 1.0]
        if data:
            self.data = data
        else:
            self.data = []
            for i in range(self.size):
                self.data.append(self.yMin)

    def randomColor(self):
        r = g = b = 3
        while r + g + b > 2.5:
            r = random.random()
            g = random.random()
            b = random.random()
        self.fg = [r, g, b]
    
    def updateData(self):
        # How much variation can be introduced per step. Must be a float between
        # 0.0 and 1.0, where 0.0 is "no change", and 1.0 is "up to 100% of the y
        # range".
        scaleFactor = 0.25
        for i in range(self.size):
            randInRange = random.random() * self.yRange + self.yMin
            self.data[i] += randInRange * scaleFactor - (self.yRange *
                                                         scaleFactor / 2)
            self.data[i] = min(self.yMax, max(self.yMin, self.data[i]))

    def draw(self, left, right, top, bottom, filled=True):
        if filled:
            # Draw the graph borders.
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINES)
            glVertex2f(left, top)
            glVertex2f(right, top)
            glVertex2f(left, bottom)
            glVertex2f(right, bottom)
            glEnd()

        # This is where the y-axis is drawn and the graph data's right side
        # ends.
        dataRight = right - (right - left) * 0.05

        # Draw the graph's y-axis.
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(dataRight, top)
        glVertex2f(dataRight, bottom)
        yCount = self.yMin
        hashRight = right - (right - dataRight) * 0.5
        #yInc = self.yStep / self.yRange
        """
        while yCount <= self.yMax:
            glVertex2f(dataRight, bottom + yCount * self.yRange)
            glVertex2f(hashRight, bottom + yCount * self.yRange)
            print "hash at %f" % (yCount
            yCount += self.yStep
                                  """
        glEnd()

        # Draw the graph data (first because OpenGL draws in reverse).
        #glColor3f(1.0, 0.0, 0.0)
        glColor3f(self.fg[0], self.fg[1], self.fg[2])
        if filled:
            glBegin(GL_TRIANGLE_STRIP)
        else:
            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
        for count, point in enumerate(self.data):
            curX = left + (float)(count) * (dataRight - left) / (float)(len(self.data) - 1)
            curY = bottom + point * (top - bottom)
            glVertex2f(curX, curY)
            if filled:
                glVertex2f(curX, bottom)
        glEnd()
        if not filled:
            glLineWidth(1)

        if filled:
            # Draw the graph background.
            glColor3f(self.bg[0], self.bg[1], self.bg[2])
            glBegin(GL_QUADS)
            glVertex2f(left, top)
            glVertex2f(left, bottom)
            glVertex2f(right, bottom)
            glVertex2f(right, top)
            glEnd()

        glColor3f(1.0, 1.0, 1.0)

class TimeGraph(Graph):
    def __init__(self, size=20, yMin=0.0, yMax=1.0, yStep=0.2, data=None):
        Graph.__init__(self, size, yMin, yMax, yStep, data)

    def updateData(self):
        scaleFactor = 0.25
        self.data.pop(0)
        randInRange = random.random() * self.yRange + self.yMin
        self.data.append(self.data[-1] + randInRange * scaleFactor -
                         (self.yRange * scaleFactor / 2))
        self.data[-1] = min(self.yMax, max(self.yMin, self.data[-1]))

class StepGraph(Graph):
    def __init__(self, size=20, yMin=0.0, yMax=1.0, yStep=0.2, data=None):
        Graph.__init__(self, size, yMin, yMax, yStep, data)
        self.numSteps=30
        self.updateCount = 0

    def updateData(self):
        self.updateCount = (self.updateCount + 1) % 3
        self.data.pop(0)
        if self.updateCount == 0:
            dStep = float(random.randint(0, self.numSteps / 2)) - \
                    float(self.numSteps) / 4
            self.data.append(self.data[-1] + 1.0 / dStep)
            self.data[-1] = min(1.0, max(0.0, self.data[-1]))
        else:
            self.data.append(self.data[-1])

class MultiGraph():
    def __init__(self, sets=None):
        self.sets = sets
        bgNum = random.random()
        self.fg = [random.random(), random.random(), random.random()]
        self.bg = [1.0, 1.0, 1.0]
        if not self.sets:
            self.sets = []

    def addGraph(self, graph):
        self.sets.append(graph)
        self.makeRandomColors()

    def makeRandomColors(self):
        num = len(self.sets)
        if num > 10:
            for i in range(num):
                self.sets[i].fg = [random.random(), random.random(), random.random()]
            return
        colorList = []
        fixedIndex = random.randint(0, 2)
        seed = [random.random(), random.random(), random.random()]
        step = 1.0 / float(num)
        for i in range(num):
            colorList.append([0, 0, 0])
            for j in range(3):
                if j == fixedIndex:
                    colorList[i][j] = 0.3
                else:
                    colorList[i][j] = (seed[j] + step * i) % 1.0
        for i in range(num):
            curRGB = colorList[i]
            self.sets[i].fg = curRGB
    
    def updateData(self):
        for graph in self.sets:
            graph.updateData()

    def draw(self, left, right, top, bottom):
        # Draw the graph borders.
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(left, top)
        glVertex2f(right, top)
        glVertex2f(left, bottom)
        glVertex2f(right, bottom)
        glEnd()

        # Draw the graph data (first because OpenGL draws in reverse).
        for graph in self.sets:
            graph.draw(left, right, top, bottom, False)
        
        # Draw the graph background.
        glColor3f(self.bg[0], self.bg[1], self.bg[2])
        glBegin(GL_QUADS)
        glVertex2f(left, top)
        glVertex2f(left, bottom)
        glVertex2f(right, bottom)
        glVertex2f(right, top)
        glEnd()

        glColor3f(1.0, 1.0, 1.0)
 
