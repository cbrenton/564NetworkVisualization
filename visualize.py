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

try:
    from PIL.Image import open
except ImportError, err:
    from Image import open

"""
This code is based on code from:
        http://wxpython-users.1045709.n5.nabble.com/Resizing-GLCanvas-Panel-td2341501.html
as well as:
        http://wiki.wxpython.org/GLCanvas
"""
class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        # The size of the GLCanvas is set here. Since the canvas will resize to
        # fit the window, this actually just sets the aspect ratio of the
        # canvas.
        glcanvas.GLCanvas.__init__(self, parent, -1, size=(100, 150))
        self.init = False
        # Record initial mouse position.
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        (w, h) = self.GetGLExtents()
        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, w, h)
        event.Skip()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def GetGLExtents(self):
        """Get the extents of the OpenGL canvas."""
        return self.GetClientSize()

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

    def OnInitGL(self):
        """Initialize OpenGL for use in the window."""
        glClearColor(1, 0, 0, 1)

    def OnDraw(self, *args, **kwargs):
        """Draw the window."""
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
    def __init__(self, parent=None):
        self.r = 1.0
        self.g = 0.0
        self.b = 0.0
        MyCanvasBase.__init__(self, parent)
        
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

    def update(self):
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
        self.OnDraw()

    def InitGL(self):
        # Set viewing projection
        glMatrixMode(GL_PROJECTION)

        # Use 2-dimensional orthographic projection.
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

        # Enable depth testing. This isn't really necessary, but doesn't hurt.
        glEnable(GL_DEPTH_TEST)

        # Generate texture for network graph.
        self.graphTex = self.loadImage()
        
        #glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def setupTexture(self):
        """Render-time texture environment setup"""
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # Ignore glColor calls instead of modulating them with textures.
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        
    def loadImage(self, imageName="graph.png"):
        im = open(imageName)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA",
                                                                0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX",
                                                                0, -1)
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image)
        return ID

    def OnDraw(self):
        # Clear color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up texture mapping.
        self.setupTexture()

        # Draw top graph area.
        self.drawTopGraph()

        # Draw bottom graph area.
        self.drawBottomGraphs()

        self.SwapBuffers()

    def drawTopGraph(self):
        glBindTexture(GL_TEXTURE_2D, self.graphTex)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(-1.0, 1.0)
        glTexCoord2f(0.0, 0.0); glVertex2f(-1.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex2f(1.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex2f(1.0, 1.0)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, -1)

    def drawBottomGraphs(self):
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_QUADS)
        glVertex2f(-1.0, -1.0)
        glVertex2f(-1.0, 0.0)
        glVertex2f(1.0, 0.0)
        glVertex2f(1.0, -1.0)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)

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

class InfoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is an InfoPanel object", (40,40))

class VisFrame(wx.Frame):
    def __init__(self, parent, id, title='theframe', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE,
                 name='Netflow Visualization'):

        super(VisFrame, self).__init__(parent, id, title, pos, size, style, name)

        # Create a panel and a notebook on the panel.
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # Create the page windows as children of the notebook.
        visPage = wx.Panel(nb)
        # Create the GLCanvas.
        canvas = CubeCanvas(visPage)
        # Create the node info panel.
        nodePanel = InfoPanel(visPage)
        # Add a sizer to visPage to manage its children.
        visSizer = wx.BoxSizer()
        visSizer.Add(canvas, 1, wx.SHAPED | wx.ALIGN_LEFT)
        #visSizer.Add(nodePanel, 1, wx.SHAPED | wx.ALIGN_RIGHT)
        visPage.SetSizer(visSizer)

        dataPage = InfoPanel(nb)

        # Add the pages to the notebook with the label to show on the tab
        nb.AddPage(visPage, "Visualization")
        nb.AddPage(dataPage, "Data")

        # Put the notebook in a sizer for the panel to manage the layout
        mainSizer = wx.BoxSizer()
        mainSizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(mainSizer)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

app = wx.App(0)

theFrame = VisFrame(None, -1, size=(600,600), name="The Frame")
#theFrame = VisFrame(None, -1, size=(600,600), style=wx.DEFAULT_FRAME_STYLE ^
#                 wx.RESIZE_BORDER, name="The Frame")
theFrame.Show()

app.MainLoop()
