# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1938, 519)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_1 = Painter(self.centralwidget)
        self.frame_1.setGeometry(QtCore.QRect(20, 20, 341, 341))
        self.frame_1.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.label_frame_1 = QtWidgets.QLabel(self.frame_1)
        self.label_frame_1.setGeometry(QtCore.QRect(0, 10, 341, 331))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.label_frame_1.setFont(font)
        self.label_frame_1.setText("")
        self.label_frame_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_frame_1.setObjectName("label_frame_1")
        self.frame_2 = Painter(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(420, 20, 341, 341))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_frame_2 = QtWidgets.QLabel(self.frame_2)
        self.label_frame_2.setGeometry(QtCore.QRect(0, 10, 341, 331))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.label_frame_2.setFont(font)
        self.label_frame_2.setText("")
        self.label_frame_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_frame_2.setObjectName("label_frame_2")
        self.frame_3 = Painter(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(820, 20, 341, 341))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_frame_3 = QtWidgets.QLabel(self.frame_3)
        self.label_frame_3.setGeometry(QtCore.QRect(0, 0, 341, 331))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.label_frame_3.setFont(font)
        self.label_frame_3.setText("")
        self.label_frame_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_frame_3.setObjectName("label_frame_3")
        self.label_result = QtWidgets.QLabel(self.centralwidget)
        self.label_result.setGeometry(QtCore.QRect(1360, 90, 531, 231))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.label_result.setFont(font)
        self.label_result.setObjectName("label_result")
        self.pushButton_enter = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_enter.setGeometry(QtCore.QRect(570, 380, 1351, 131))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.pushButton_enter.setFont(font)
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.label_equals = QtWidgets.QLabel(self.centralwidget)
        self.label_equals.setGeometry(QtCore.QRect(1190, 100, 151, 231))
        font = QtGui.QFont()
        font.setPointSize(80)
        self.label_equals.setFont(font)
        self.label_equals.setObjectName("label_equals")
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(20, 380, 521, 131))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.pushButton_clear.setFont(font)
        self.pushButton_clear.setObjectName("pushButton_clear")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_result.setText(_translate("MainWindow", "??"))
        self.pushButton_enter.setText(_translate("MainWindow", "="))
        self.label_equals.setText(_translate("MainWindow", "="))
        self.pushButton_clear.setText(_translate("MainWindow", "Clear"))

from painter import Painter
