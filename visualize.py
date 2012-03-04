#!/usr/bin/python2.7

import wx
import sys
import random

from wx import glcanvas

# The Python OpenGL package can be found at
# http://PyOpenGL.sourceforge.net/
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

"""
This code is based on code from:
        http://wxpython-users.1045709.n5.nabble.com/Resizing-GLCanvas-Panel-td2341501.html
as well as:
        http://wiki.wxpython.org/GLCanvas
"""
class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        #glcanvas.GLCanvas.__init__(self, parent, -1, size=(100,300))
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(100, 150))
        self.init = False
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None

        self.r = 1.0
        self.g = 0.0
        self.b = 0.0

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

    def drawColor(self):
        glColor3f(self.r, self.g, self.b)
        print "glColor3f(%d, %d, %d)" % (self.r, self.g, self.b)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        #minDimension = min(self.GetGLExtents())
        (w, h) = self.GetGLExtents()
        if self.GetContext():
            self.SetCurrent()
            #glViewport(0, 0, minDimension, minDimension)
            #glViewport(0, 0, (int)(size[0] * 0.7), size[1])
            glViewport(0, 0, w, h)
        event.Skip()

    def update(self):
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
        self.OnDraw()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()
        x = evt.GetX()
        y = evt.GetY()
        print "left click at %d, %d" % (x, y)

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)

    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.GetClientSize()

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        print keycode
        if keycode == wx.WXK_SPACE:
            print "you pressed the spacebar!"
        elif chr(keycode) == 'Q':
            print "quitting"
            app.Exit()
        elif chr(keycode) == 'R':
            self.update()
        else:
            print chr(keycode)
        event.Skip()

    # GLFrame OpenGL Event Handlers

    def OnInitGL(self):
        """Initialize OpenGL for use in the window."""
        glClearColor(1, 0, 0, 1)

    def OnDraw(self, *args, **kwargs):
        "Draw the window."
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing an example triangle in the middle of the screen
        glBegin(GL_TRIANGLES)
        glColor(0, 0, 0)
        glVertex(-.25, -.25)
        glVertex(.25, -.25)
        glVertex(0, .25)
        glEnd()

        self.SwapBuffers()

class CubeCanvas(MyCanvasBase):
    def InitGL(self):
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        (w, h) = self.GetGLExtents()
        aspect = (float)(w) / (float)(h)
        gluOrtho2D(-1.0, 1.0, -aspect, aspect)

        glEnable(GL_DEPTH_TEST)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw bottom graph area
        #glColor3f(self.r, self.g, self.b)
        self.drawColor()
        print "Drawing color"
        glBegin(GL_QUADS)
        glVertex2f(-1.0, -1.0)
        glVertex2f(-1.0, 0.0)
        glVertex2f(1.0, 0.0)
        glVertex2f(1.0, -1.0)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)

        self.SwapBuffers()

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageOne object", (20,20))

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40,40))

app = wx.App(0)

frame = wx.Frame(None, -1, size=(600,600), style = wx.RESIZE_BORDER)

# Here we create a panel and a notebook on the panel
p = wx.Panel(frame)
nb = wx.Notebook(p)

# create the page windows as children of the notebook
visPage = wx.Panel(nb)
canvas = CubeCanvas(visPage)
visSizer = wx.BoxSizer()
#visSizer.Add(canvas, 1, wx.SHAPED | wx.ALIGN_CENTER)
visSizer.Add(canvas, 1, wx.SHAPED | wx.ALIGN_LEFT)
visPage.SetSizer(visSizer)

dataPage = PageTwo(nb)

# add the pages to the notebook with the label to show on the tab
nb.AddPage(visPage, "Visualization")
nb.AddPage(dataPage, "Data")

# finally, put the notebook in a sizer for the panel to manage
# the layout
mainSizer = wx.BoxSizer()
mainSizer.Add(nb, 1, wx.EXPAND)
p.SetSizer(mainSizer)

frame.Show(True)

app.MainLoop()
