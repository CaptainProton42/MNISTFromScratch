from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
from scipy import ndimage
import datetime
import struct
sys.path.append("modules")
import idx
sys.path.append("Survey")
import uisurvey

now = datetime.datetime.now

class GUI(QtWidgets.QMainWindow, uisurvey.Ui_MainWindow):

    def clearAll(self):
        self.frame_1.clearCanvas()
        self.frame_2.clearCanvas()
        self.frame_3.clearCanvas()
        self.frame_4.clearCanvas()
        
    def get_image(self, painterWidget):
        img = QtGui.QImage(painterWidget.geometry().width(), painterWidget.geometry().height(), QtGui.QImage.Format_Grayscale8)
        img.fill(QtCore.Qt.white)
        painter = QtGui.QPainter()
        painter.begin(img)
        painterWidget.drawLines(painter)
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

        # normalize
        #arr = arr / 255

        # shift by weight (maybe better shift by bounding box?)
        com = ndimage.measurements.center_of_mass(arr)
        shift = np.subtract((14, 14),  com)
        arr = ndimage.interpolation.shift(arr, shift)

        return arr

    def showImage(self, img_arr, frame):
        arr_bits = 255 - img_arr
        arr_bits = arr_bits.tobytes()
  
        centered_img = QtGui.QImage(arr_bits, 28, 28, QtGui.QImage.Format_Grayscale8)

        frame.showImage(centered_img)

    def saveSamples(self):
        img_file = idx.file(dtype=">u1", datashape=[28, 28])
        lbl_file = idx.file(dtype=">u1", datashape=[])

        frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4]
        index = 0
        for frame in frames:
            img = self.get_image(frame)
            print(img.shape)
            img_file.append([img])
            lbl_file.append([index])

            frame.clearCanvas()

            self.showImage(img, frame)

            index += 1

        str_now = now().strftime("%Y%m%d%H%M%S")

        idx.write("Survey/samples/%s.idx3-ubyte" % str_now, img_file)
        idx.write("Survey/samples/%s.idx1-ubyte" % str_now, lbl_file)

    def openSamples(self):
        dlg = QtWidgets.QFileDialog()
        file_path = dlg.getOpenFileName(self, 'Open Sample', 'survey/samples',
                                        filter='idx3 (*.idx3-ubyte)')[0]

        if file_path:
            img = idx.read(file_path).body

            if not (img.shape == (4, 28, 28)):
                print("Data shape doesn't match. Are you opening the correct file?")
                return 

            frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4]
            for i in range(len(frames)):
                self.showImage(img[i], frames[i])

    # Constructor
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.geometry().width(), self.geometry().height())

        self.pushButton_save.clicked.connect(self.saveSamples)
        self.pushButton_clear.clicked.connect(self.clearAll)
        self.pushButton_open.clicked.connect(self.openSamples)

app = QtWidgets.QApplication(sys.argv)
MainWindow = GUI()
MainWindow.show()

app.exec_()