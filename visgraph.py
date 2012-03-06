#!/usr/bin/env python

import random

# The Python OpenGL package can be found at
# http://PyOpenGL.sourceforge.net/
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Graph():
    def __init__(self, size=20, data=None):
        self.size = size
        self.fg = [0.2, 0.4, 0.4]
        self.bg = [1.0, 1.0, 1.0]
        if data:
            self.data = data
        else:
            self.data = []
            for i in range(self.size):
                self.data.append(0.0)
        self.randomColor()

    def randomColor(self):
        self.fg = [random.random(), random.random(), random.random()]
        #bgVal = random.random() / 2.0
        #self.bg = [bgVal, bgVal, bgVal]
    
    def randomize(self):
        for i in range(self.size):
            self.data[i] = (random.random())

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

        # Draw the graph data (first because OpenGL draws in reverse).
        #glColor3f(1.0, 0.0, 0.0)
        glColor3f(self.fg[0], self.fg[1], self.fg[2])
        if filled:
            glBegin(GL_TRIANGLE_STRIP)
        else:
            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
        for count, point in enumerate(self.data):
            curX = left + (float)(count) * (right - left) / (float)(len(self.data) - 1)
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

class MultiGraph():
    def __init__(self, sets=None):
        self.sets = sets
        bgNum = random.random()
        self.fg = [random.random(), random.random(), random.random()]
        self.bg = [0.9, 0.9, 0.9]
        if not self.sets:
            self.sets = []

    def addGraph(self, graph):
        self.sets.append(graph)
    
    def randomize(self):
        for graph in self.sets:
            graph.randomize()

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
 
