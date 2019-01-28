from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
from scipy import ndimage
import datetime
import struct
sys.path.append("modules")
import idx
sys.path.append("calculator")
import gui
sys.path.append("extension")
import pyceptron

now = datetime.datetime.now

class GUI(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    # Constructor
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        # Connect signals
        self.pushButton_enter.clicked.connect(self.calculate)
        self.pushButton_clear.clicked.connect(self.clear)

        self.network_digits = pyceptron.Network([784, 300, 10], activation="ReLU", softmax=1)
        self.network_operators = pyceptron.Network([784, 100, 4], activation="ReLU", softmax=1)

        self.network_digits.load_state("states/784_300_10_sgd_ReLU_softmax_229.state")
        self.network_operators.load_state("states/operators.state")

    def calculate(self):
        digit_1 = self.guess(self.frame_1, self.network_digits)
        digit_2 = self.guess(self.frame_3, self.network_digits)
        operator = self.guess(self.frame_2, self.network_operators)

        print(digit_1)
        print(digit_2)
        print(operator)

        result = None
        self.clear()

        if operator == 0:
            result =  int(digit_1) + int(digit_2)
            self.label_frame_2.setText("+")
        elif operator == 1:
            result =  int(digit_1) - int(digit_2)
            self.label_frame_2.setText("-")
        elif operator == 2:
            result = int(digit_1) * int(digit_2)
            self.label_frame_2.setText("*")
        elif operator == 3:
            if not int(digit_2) == 0:
                result = int(digit_1) / int(digit_2)
            self.label_frame_2.setText("/")

        self.label_frame_1.setText(str(digit_1))
        self.label_frame_3.setText(str(digit_2))

        self.label_result.setText(str(result))

    def clear(self):
        self.frame_1.clearCanvas()
        self.frame_2.clearCanvas()
        self.frame_3.clearCanvas()
        self.label_frame_1.setText("")
        self.label_frame_2.setText("")
        self.label_frame_3.setText("")

    def guess(self, panel, network):
        img = QtGui.QImage(panel.geometry().width(), panel.geometry().height(), QtGui.QImage.Format_Grayscale8)
        img.fill(QtCore.Qt.white)
        painter = QtGui.QPainter()
        painter.begin(img)
        panel.drawLines(painter)
        painter.end()
        
        scaled_img = img.scaledToHeight(28, mode=QtCore.Qt.SmoothTransformation)
        scaled_img = scaled_img.convertToFormat(QtGui.QImage.Format_Grayscale8)

        # image to buffer
        b = scaled_img.bits()
        # sip.voidptr must know size to support python buffer interface
        b.setsize(28 * 28)
        # buffer to array
        arr = np.frombuffer(b, np.uint8).reshape((28, 28))
    
        arr = 255 - arr

        # shift by weight (maybe better shift by bounding box?)
        com = ndimage.measurements.center_of_mass(arr)
        shift = np.subtract((14, 14),  com)
        arr = ndimage.interpolation.shift(arr, shift)

        # normalize
        arr = arr / 255

        prediction = network.predict(arr.flatten().tolist())
        index = np.argmax(prediction)

        return index

app = QtWidgets.QApplication(sys.argv)
MainWindow = GUI()
MainWindow.show()

app.exec_()