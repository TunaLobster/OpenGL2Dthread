# Charles Johnson
# 10/15/2018
# Written for MAE 3403 Fall 2018

from time import sleep

pauseVal = False


def spinit(glwindow, app):
    # simple animation - by rotating the image
    # about the center of the circle

    for i in range(120):
        if not pauseVal:
            angle = glwindow.glRotate()
            angle += 3
            glwindow.glRotate(angle, 0.5, 0.5)
            app.processEvents()
            sleep(0.03)
        else:
            sleep(0.03)
            continue


# class Worker(QObject):
#     """
#     Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
#     """
#
#     sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
#     sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
#     sig_msg = pyqtSignal(str)  # message to be shown to user
#
#     def __init__(self, id: int):
#         super().__init__()
#         self.__id = id
#         self.__abort = False
#
#     @pyqtSlot()
#     def work(self):
#         """
#         Pretend this worker method does work that takes a long time. During this time, the thread's
#         event loop is blocked, except if the application's processEvents() is called: this gives every
#         thread (incl. main) a chance to process events, which in this sample means processing signals
#         received from GUI (such as abort).
#         """
#         thread_name = QThread.currentThread().objectName()
#         thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
#         self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))
#
#         for step in range(100):
#             time.sleep(0.1)
#             self.sig_step.emit(self.__id, 'step ' + str(step))
#
#             # check if we need to abort the loop; need to process events to receive signals;
#             app.processEvents()  # this could cause change to self.__abort
#             if self.__abort:
#                 # note that "step" value will not necessarily be same for every thread
#                 self.sig_msg.emit('Worker #{} aborting work at step {}'.format(self.__id, step))
#                 break
#
#
#         self.sig_done.emit(self.__id)
#
#     def abort(self):
#         self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
#         self.__abort = True


# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we connect a signal
of a QSlider to a slot of a QLCDNumber.

Author: Jan Bodnar
Website: zetcode.com
Last edited: January 2017
"""

# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
#                              QVBoxLayout, QApplication)
#
#
# class Example(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         lcd = QLCDNumber(self)
#         sld = QSlider(Qt.Horizontal, self)
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(lcd)
#         vbox.addWidget(sld)
#
#         self.setLayout(vbox)
#         sld.valueChanged.connect(lcd.display)
#
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('Signal and slot')
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we display the x and y 
coordinates of a mouse pointer in a label widget.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        x = 0
        y = 0

        self.text = "x: {0},  y: {1}".format(x, y)

        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        self.setMouseTracking(True)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('Event object')
        self.show()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
