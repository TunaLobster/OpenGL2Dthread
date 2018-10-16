import numpy as np
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class gl2D():

    def __init__(self, glWidget, drawCallback,
                 allowDistortion=False,
                 xmin=0, xmax=1, ymin=0, ymax=1,
                 rotate=0, zoom=1.0,
                 backgroundcolor=(0.65, 0.65, 0.65)):

        self.glWindowWidget = glWidget
        self.drawCallback = drawCallback
        self.allowDistortion = allowDistortion
        self.glZoomval = zoom  # zoom factor
        self.glRotateval = rotate  # rotation factor in Degrees
        self.glXmin = xmin  # Width of the object to be drawn
        self.glXmax = xmax  # Height of the object to be drawn
        self.glYmin = ymin  # X-location of the center of the object to be drawn
        self.glYmax = ymax  # Y-location of the center of the object to be drawn
        self.glWidth = xmax - xmin  # Width of the object to be drawn
        self.glHeight = ymax - ymin  # Height of the object to be drawn
        self.glXcenter = (xmax + xmin) / 2  # X-location of the center of the object to be drawn
        self.glYcenter = (ymax + ymin) / 2  # Y-location of the center of the object to be drawn
        self.glZoomX = self.glXcenter
        self.glZoomY = self.glYcenter
        self.glRotX = self.glXcenter
        self.glRotY = self.glYcenter
        self.glBackgroundColor = backgroundcolor

        self.glViewReady = False
        self.glModel = None  # storing the model matrix
        self.glProjection = None  # storing the projection matrix
        self.glView = None  # storing the Viewport array

        self.glWindowWidget.initializeGL = self.glInit  # initialize callback
        self.glWindowWidget.paintGL = self.paintGL  # paint callback

    def glInit(self):
        glutInit(sys.argv)

    def glUpdate(self):
        self.glWindowWidget.update()

    def glZoom(self, zoom, xcenter=None, ycenter=None):
        # zoom the image about the chosen center
        if zoom is None: return self.glZoomval  # return the zoom factor
        self.glZoomval = zoom
        if xcenter is not None: self.glZoomX = xcenter
        if ycenter is not None: self.glZoomY = ycenter
        self.glViewReady = False
        self.glUpdate()

    def glRotate(self, angle=None, xcenter=None, ycenter=None):
        # rotate the image about the chosen center
        if angle is None: return self.glRotateval  # return the rotation angle
        self.glRotateval = angle
        if xcenter is not None: self.glRotX = xcenter
        if ycenter is not None: self.glRotY = ycenter
        self.glViewReady = False
        self.glUpdate()

    def setViewSize(self, xmin, xmax, ymin, ymax, allowDistortion=False):
        self.glXmin = xmin
        self.glXmax = xmax
        self.glYmin = ymin
        self.glYmax = ymax
        self.glWidth = xmax - xmin  # Width of the object to be drawn
        self.glHeight = ymax - ymin  # Height of the object to be drawn
        self.glXcenter = (xmax + xmin) / 2  # X-location of the center of the object to be drawn
        self.glYcenter = (ymax + ymin) / 2  # Y-location of the center of the object to be drawn

        self.allowDistortion = allowDistortion
        self.glViewReady = False
        self.glUpdate()

    def setupGLviewing(self):

        if self.glViewReady == True:  return  # nothing to do

        # setup the drawing window size and scaling
        windowWidth = self.glWindowWidget.frameSize().width()
        windowHeight = self.glWindowWidget.frameSize().height()
        glViewport(1, 1, windowWidth - 1, windowHeight - 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        top = self.glYmax
        bottom = self.glYmin
        right = self.glXmax
        left = self.glXmin

        if self.allowDistortion == False:  # force no shape distortion
            windowShape = windowWidth / windowHeight
            drawingShape = self.glWidth / self.glHeight
            if drawingShape > windowShape:
                newheight = self.glHeight * drawingShape / windowShape
                top = (top + bottom) / 2 + newheight / 2
                bottom = top - newheight
            else:
                newwidth = self.glWidth * windowShape / drawingShape
                right = (right + left) / 2 + newwidth / 2
                left = right - newwidth

        glOrtho(left, right, bottom, top, -1, 1)  # simple 2D projection

        # perform zoom and rotation about the respective centers
        glTranslatef(self.glZoomX, self.glZoomY, 0)
        glScalef(self.glZoomval, self.glZoomval, 1)
        glTranslatef(-self.glZoomX, -self.glZoomY, 0)
        glTranslatef(self.glRotX, self.glRotY, 0)
        glRotatef(self.glRotateval, 0, 0, 1)
        glTranslatef(-self.glRotX, -self.glRotY, 0)

        # save the transformation matrices to make mouse tracking faster
        self.glModel = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.glProjection = glGetDoublev(GL_PROJECTION_MATRIX)
        self.glView = glGetIntegerv(GL_VIEWPORT)

        self.glViewReady = True  # all done ... until things change

    def paintGL(self):
        # this is a firly generic widow setup code for 2D graphics
        # the specific drawing code should be placed in the drawCallback() function
        # drawCallback() is called on the last line of this function
        self.setupGLviewing()  # what it says!
        bc = self.glBackgroundColor
        glClearColor(bc[0], bc[1], bc[2], 0)  # set the background color
        glClear(GL_COLOR_BUFFER_BIT)  # clear the drawing

        self.drawCallback()  # draw the user's drawing

    def UnProjectMouse(self, wx, wy):
        vx = GLdouble(wx)
        vy = self.glView[3] - GLdouble(wy)
        vz = GLdouble(0)
        x, y, z = gluUnProject(vx, vy, vz, model=self.glModel, proj=self.glProjection, view=self.glView)
        return x, y


def gl2DText(text, x, y, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2d(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


def gl2DCircle(xcenter, ycenter, radius, fill=False, faces=24):
    theta = 0

    if fill:
        glBegin(GL_POLYGON);
    else:
        glBegin(GL_LINE_STRIP);

    glVertex2f(xcenter + np.cos(theta) * radius, ycenter + np.sin(theta) * radius);
    for i in range(1, faces + 1):
        theta = i / faces * 2 * np.pi
        glVertex2f(xcenter + np.cos(theta) * radius, ycenter + np.sin(theta) * radius);
    glEnd();
