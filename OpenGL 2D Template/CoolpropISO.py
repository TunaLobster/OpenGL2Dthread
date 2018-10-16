import CoolProp
import PyQt5
import OpenGL

from CoolProp.Plots import PropertyPlot

import warnings

import numpy as np
from time import sleep

import sys


from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QEvent


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL_2D_class import gl2D, gl2DText, gl2DCircle

from OpenGL_2D_ui import Ui_Dialog


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        # setup the GUI
        self.ui.setupUi(self)

        # ************************************************************************
        # create and initialize a gl2D window object for each GLWidget in the GUI
        #                   the widget name     the drawing callback
        self.glwindow1 = gl2D(self.ui.openGLWidget, self.Drawit, allowDistortion= True,
                              xmin=50, xmax = 550, ymin = 0, ymax = 4,
                              backgroundcolor = (0.9, 0.9, 0.9))
        # ************************************************************************

        # define any additional data
        # or perform any tasks that your program might need
        self.showlabels = True
        self.xPH = None
        self.yPY = None
        self.getPHdata() #read the data

        # and define any callbacks or other necessary setup
        self.assign_widgets()

        # show the GUI
        self.show()

    def assign_widgets(self):
        self.ui.pushButton_Exit.clicked.connect(self.ExitApp)
        self.ui.horizontalSlider_zoom.valueChanged.connect(self.ZoomSlider)
        self.ui.horizontalSlider_rotate.valueChanged.connect(self.RotationSlider)
        self.ui.checkBox_showlabels.stateChanged.connect(self.Checkboxes)
        self.ui.openGLWidget.installEventFilter(self)  # to read the mouse location
        self.ui.openGLWidget.installEventFilter(self)  # to read the mouse location
        self.ui.openGLWidget.setMouseTracking(True)

    def eventFilter(self, source, event):  # handle events that can't be CONNECTED
        if event.type() == QEvent.MouseMove:  # read the mouse location
            pos = event.pos()
            x, y = self.glwindow1.UnProjectMouse(pos.x(), pos.y())
            self.ui.MouseLocation.setText("{:.1f}".format(x) + ", {:.1f}".format(10.0 ** y))
        return super(QDialog, self).eventFilter(source, event)  #required!


    def ZoomSlider(self):  # I used a slider to control the zooming
        zoomval = float((self.ui.horizontalSlider_zoom.value()) / 200 + 0.25)
        self.glwindow1.glZoom(zoomval)


    def RotationSlider(self):  # I used a slider to control rotation
        angle= float((self.ui.horizontalSlider_rotate.value()))
        self.glwindow1.glRotate(angle)


    def Checkboxes(self):
        if self.ui.checkBox_showlabels.isChecked():
            self.showlabels = True
        else:
            self.showlabels = False
        self.glwindow1.glUpdate()  # update the picture

    def Drawit(self):
        self.drawPHdiagram()



    def ExitApp(self):
        app.exit()

    def getPHdata(self):
        ncurves = 10
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plot = PropertyPlot('R134a', 'ph')
            plot.calc_isolines(num = ncurves)
            #plot.show()


        #extract the isolines from coolprop, and plot them with pyplot
            for i in range(0,10):
                xi=(plot.isolines[21])[i].x/1000
                yi=(plot.isolines[21])[i].y/1000
                if self.xPH is None:
                    self.xPH = np.array(xi)
                    self.yPH = np.array(yi)
                else:
                    self.xPH = np.vstack((self.xPH, xi))
                    self.yPH = np.vstack((self.yPH,yi))

                xi=(plot.isolines[19])[i].x/1000
                yi=(plot.isolines[19])[i].y/1000
                self.xPH = np.vstack((self.xPH, xi))
                self.yPH = np.vstack((self.yPH, yi))

                xi=(plot.isolines[34])[i].x/1000
                yi=(plot.isolines[34])[i].y/1000
                self.xPH = np.vstack((self.xPH, xi))
                self.yPH = np.vstack((self.yPH, yi))

                xi=(plot.isolines[36])[i].x/1000
                yi=(plot.isolines[36])[i].y/1000
                self.xPH = np.vstack((self.xPH, xi))
                self.yPH = np.vstack((self.yPH, yi))
            #next i
        #end with
        return
    #end getPHdata()


    def drawPHdiagram(self):

        for i in range(0,4*10):
            #plot the bulk of the data
            glColor3f(0.65, 0.65, 0.65)
            glLineWidth(0.5)
            glBegin(GL_LINE_STRIP)  # begin drawing disconnected lines
            for j in range(len(self.xPH[i])) :
                glVertex2f(self.xPH[i,j], np.log10(self.yPH[i,j]))
            glEnd()

            #plot the saturation dome in bold
            # (stored in curves 0 and 36)
            glColor3f(0.0, 0.0, 0.0)
            glLineWidth(1.0)

            i = 0 #make this curve darker
            glBegin(GL_LINE_STRIP)  # begin drawing disconnected lines
            for j in range(len(self.xPH[i])) :
                glVertex2f(self.xPH[i,j], np.log10(self.yPH[i,j]))
            glEnd()
            i = 36 #make this curve darker
            glBegin(GL_LINE_STRIP)  # begin drawing disconnected lines
            for j in range(len(self.xPH[i])) :
                glVertex2f(self.xPH[i,j], np.log10(self.yPH[i,j]))
            glEnd()
# end draw PH diagram



if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())


