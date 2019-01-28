from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
from scipy import ndimage
sys.path.append('modules')
import mnist
sys.path.append('extension')
import pyceptron
sys.path.append("recognition")
import gui

class GUI(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def setEta(self, value):
        self.eta = value

    def setEpochs(self, value):
        self.epochs = value

    def togglePreview(self):
        if (self.Preview_CheckBox.isChecked()):
            self.previewEnabled = True
        else:
            self.previewEnabled = False

    def trainNetwork(self):
        training_set = mnist.read(path="./mnist")
        vectorized_training_set = mnist.read(path="./mnist")

        self.network.train(vectorized_training_set, epochs=self.epochs, batchsize=1, eta = self.eta / 60000)

        self.Status_Label.setText("Training finished!")
        self.StatusLamp.setGreen()

    def guess(self):
        img = QtGui.QImage(self.canvasPanel.geometry().width(), self.canvasPanel.geometry().height(), QtGui.QImage.Format_Grayscale8)
        img.fill(QtCore.Qt.white)
        painter = QtGui.QPainter()
        painter.begin(img)
        self.canvasPanel.drawLines(painter)
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

        if (self.previewEnabled):

            #arr_bits = arr * 255
            arr_bits = 255 - arr
            arr_bits = arr_bits.tobytes()
            

            centered_img = QtGui.QImage(arr_bits, 28, 28, QtGui.QImage.Format_Grayscale8)

            self.canvasPanel.showImage(centered_img)

        # normalize
        arr = arr / 255

        prediction = self.network.predict(arr.flatten().tolist())
        number = np.argmax(prediction)
        probability = prediction[number]

        self.Output_Label.setText("%i" % number)
        self.Bar_0.setValue(prediction[0])
        self.Bar_1.setValue(prediction[1])
        self.Bar_2.setValue(prediction[2])
        self.Bar_3.setValue(prediction[3])
        self.Bar_4.setValue(prediction[4])
        self.Bar_5.setValue(prediction[5])
        self.Bar_6.setValue(prediction[6])
        self.Bar_7.setValue(prediction[7])
        self.Bar_8.setValue(prediction[8])
        self.Bar_9.setValue(prediction[9])

    def saveState(self):
        dlg = QtWidgets.QFileDialog()
        file_path = dlg.getSaveFileName(self, "Save Network State", './states',
                                        filter="Network State (*.state)")[0]

        if file_path:              
            self.network.save_state(file_path)
            self.Status_Label.setText("Saved network state to disk!")

    def loadState(self):
        dlg = QtWidgets.QFileDialog()
        file_path = dlg.getOpenFileName(self, 'Load Network State', './states',
                                        filter='Network State (*.state)')[0]

        if file_path:
            try:
                self.network.load_state(file_path)
            except:
                self.Status_Label.setText("Incompatible state file!")
                return
        else:
            return

        self.Status_Label.setText("Loaded network state from disk!")
        self.StatusLamp.setGreen()

    def createNetwork(self):
        activation = ""
        if self.Activation_comboBox.currentIndex() == 0:
            activation = "sigmoid"
        elif self.Activation_comboBox.currentIndex() == 1:
            activation = "tanh"
        elif self.Activation_comboBox.currentIndex() == 2:
            activation = "ReLU"
        elif self.Activation_comboBox.currentIndex() == 3:
            activation = "Leaky ReLU"
        elif self.Activation_comboBox.currentIndex() == 4:
            activation = "linear"
        
        softmax = 0
        if self.Softmax_CheckBox.isChecked():
            softmax = 1
        else:
            softmax = 0

        # oofie
        architecture = list()
        current_number = list()
        architecture_string = self.Architecture_lineEdit.text()
        for char in architecture_string:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                current_number.append(int(char))
            elif char == ',':
                number = 0
                for i in range(len(current_number)):
                    number += current_number[i] * 10**(len(current_number) - 1 - i)

                architecture.append(number)

                current_number = list()
            elif char ==' ': # allow spaces
                pass
            else:
                self.Status_Label.setText("Invalid architecture string!")
                return

        number = 0
        for i in range(len(current_number)):
            number += current_number[i] * 10**(len(current_number) - 1 - i)

        architecture.append(number)
        current_number = list()

        if len(architecture) < 2 or architecture[0] != 784 or architecture[len(architecture)-1] != 10:
            self.Status_Label.setText("Architecture doesn't match dataset! (Should be 784,..,10.)")
            return

        self.network = pyceptron.Network(architecture, activation=activation, softmax=softmax)
        self.Status_Label.setText("Network created!")
        self.StatusLamp.setRed()

    def connectSignals(self):
        self.Clear_Button.clicked.connect(self.canvasPanel.clearCanvas)
        self.Guess_Button.clicked.connect(self.guess)
        self.Train_Button.clicked.connect(self.trainNetwork)
        self.Save_Button.clicked.connect(self.saveState)
        self.Load_Button.clicked.connect(self.loadState)
        self.Preview_CheckBox.clicked.connect(self.togglePreview)
        self.Eta_DoubleSpinBox.valueChanged.connect(self.setEta)
        self.Epochs_SpinBox.valueChanged.connect(self.setEpochs)
        self.Activation_comboBox.currentIndexChanged.connect(self.createNetwork)
        self.Softmax_CheckBox.toggled.connect(self.createNetwork)
        self.Architecture_lineEdit.editingFinished.connect(self.createNetwork)

    # Constructor
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.geometry().width(), self.geometry().height())
        self.eta = 0.5
        self.epochs = 1
        self.Eta_DoubleSpinBox.setValue(self.eta)
        self.Epochs_SpinBox.setValue(self.epochs)
        self.connectSignals()

        self.previewEnabled = False

        self.isMouseing = False

        self.eta = 0.5
        self.epochs = 1
        self.network = None

        self.createNetwork()

app = QtWidgets.QApplication(sys.argv)
MainWindow = GUI()
MainWindow.show()

app.exec_()