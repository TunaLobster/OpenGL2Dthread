# from fbs_runtime.application_context import ApplicationContext

from time import sleep

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL_2D_class import gl2D, gl2DText, gl2DCircle
from OpenGL_2D_ui import Ui_Dialog
from PyQt5.QtCore import QEvent, Qt, QObject, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog


# import OpenGLthread
def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print([repr(arg) for arg in args])


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """
    def __init__(self):
        super().__init__()
        self.abortval = False

    @pyqtSlot(gl2D)
    def rotate(self, window):
        """
        rotation is the work. Modified from Oliver on stackoverflow
        https://stackoverflow.com/questions/41526832/pyqt5-qthread-signal-not-working-gui-freeze
        """
        # print(type(window))
        while not self.abortval:
            angle = window.glRotate()
            angle += 1
            window.glRotate(angle, 0.5, 0.5)
            app.processEvents()
            sleep(0.03)

    def abort(self):
        self.abortval = True


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        # setup the GUI
        self.ui.setupUi(self)

        # ************************************************************************
        # create and initialize a gl2D window object for each GLWidget in the GUI
        #                   the widget name     the drawing callback
        # self.glwindow1 = gl2D(self.ui.openGLWidget, self.Drawit,
        #                   ready = True, allowDistortion = False,
        #                   xmin = 0, xmax = 1, ymin = 0, ymax = 1,
        #                   rotate = 0, zoom = 1.0, backgroundcolor = (0.65, 0.65, 0.65)):
        #

        self.glwindow1 = gl2D(self.ui.openGLWidget, self.Drawit,
                              xmin=0, xmax=1, ymin=0, ymax=2)
        self.__thread = None
        # ************************************************************************

        # define any additional data your program might need
        self.showlabels = True

        # and define any callbacks or other necessary setup
        self.assign_widgets()

        # show the GUI
        self.show()

    def assign_widgets(self):
        self.ui.pushButton_Exit.clicked.connect(self.ExitApp)
        self.ui.pushButton_Animate.clicked.connect(self.Spinit)
        self.ui.horizontalSlider_zoom.valueChanged.connect(self.glZoomSlider)
        self.ui.horizontalSlider_rotate.valueChanged.connect(self.glRotateSlider)
        self.ui.checkBox_showlabels.stateChanged.connect(self.Checkboxes)
        self.ui.openGLWidget.installEventFilter(self)  # to read the mouse location
        self.ui.openGLWidget.setMouseTracking(True)  # to read the mouse location

    def eventFilter(self, source, event):  # handle events that can't be CONNECTED
        if event.type() == QEvent.MouseMove:  # to read the mouse location
            pos = event.pos()
            x, y = self.glwindow1.UnProjectMouse(pos.x(), pos.y())
            self.ui.MouseLocation.setText("{:.1f}".format(x) + ", {:.1f}".format(y))
        return super(QDialog, self).eventFilter(source, event)

    def glZoomSlider(self):  # I used a slider to control the zooming
        zoomval = float((self.ui.horizontalSlider_zoom.value()) / 200 + 0.25)
        self.glwindow1.glZoom(zoomval)

    def glRotateSlider(self):  # I used a slider to control rotation
        angle = -float((self.ui.horizontalSlider_rotate.value()))
        self.glwindow1.glRotate(angle, 0.5, 0.5)

    def Checkboxes(self):  # used a checkbox to control visibility of the label
        if self.ui.checkBox_showlabels.isChecked():
            self.showlabels = True
        else:
            self.showlabels = False
        self.glwindow1.glUpdate()  # update the picture

    def Drawit(self):
        # Draw the house
        glColor3f(0, 0.90, 0.25)
        glLineWidth(4)
        glBegin(GL_LINE_STRIP)  # begin drawing connected lines
        # use GL_LINE for drawing a series of disconnected lines
        glVertex2f(0, 0)
        glVertex2f(0, 1)
        glVertex2f(1, 1)
        glVertex2f(1, 0)
        glVertex2f(0, 0)
        glEnd()
        # change the color and linewidth
        glColor3f(0.75, 0.15, 0.250)
        glLineWidth(20)
        glBegin(GL_LINE_STRIP)  # begin drawing connected lines
        glVertex2f(0, 1)
        glVertex2f(0.5, 1.7)
        glVertex2f(1, 1)
        glEnd()
        # Draw a filled circle
        glColor3f(0.75, 0.15, 0.250)
        glLineWidth(2)
        gl2DCircle(0.5, 0.5, 0.4, fill=True)
        # Draw two unfilled circles
        glColor3f(1, 1, 1)
        glLineWidth(1.5)
        gl2DCircle(0.5, 0.5, 0.3)
        gl2DCircle(0.5, 0.5, 0.2)

        if self.showlabels:
            # draw the label on the house
            glColor3f(1, 1, 1)
            gl2DText('House', 0.2, 0.5)

    # end render scene

    @pyqtSlot()
    def abort_workers(self):
        # for thread, worker in self.__thread:  # note nice unpacking by Python, avoids indexing
        #     thread.terminate()
            # thread.wait()  # <- so you need to wait for it to *actually* quit
        for thread, worker in self.__thread:
            thread.exit()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_P:
            print('Pressed P')
            self.abort_workers()
            app.processEvents()

    def Spinit(self):
        self.__thread = []
        worker = Worker()
        thread = QThread()
        self.__thread.append((thread, worker))
        # self.__thread.append(thread)
        worker.moveToThread(thread)
        # print(type(self.glwindow1))
        thread.started.connect(worker.rotate(self.glwindow1))
        thread.start()
        sleep(2)
        thread.stop()
        thread.wait()

    def ExitApp(self):
        # app.processEvents()
        app.exit()


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())

# class AppContext(ApplicationContext):
#     def run(self):
#         # app = QApplication(sys.argv)
#         # app.aboutToQuit.connect(app.deleteLater)
#         app = self.app
#         main_win = main_window()
#         return app.exec_()
#
#
# if __name__ == "__main__":
#     appcontxt = AppContext()
#     sys.exit(appcontxt.run())
