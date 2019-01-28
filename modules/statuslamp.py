from PyQt5 import QtGui, QtCore, QtWidgets

class StatusLamp(QtWidgets.QFrame):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        
        self.color = QtGui.QColor()
        self.color.setNamedColor("lightcoral")
        self.value = 0.0

    def setNamedColor(self, color):
        self.color.setNamedColor(color)
        self.repaint()

    def setRGBColor(self, r, g, b):
        self.color = QtGui.QColor(r, g, b)
        self.repaint()

    def setRed(self):
        self.color.setNamedColor("lightcoral")
        self.repaint()

    def setYellow(self):
        self.color.setNamedColor("goldenrod")
        self.repaint()
    
    def setGreen(self):
        self.color.setNamedColor("limegreen")
        self.repaint()

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)     

        pen = QtGui.QPen(self.color)
        painter.setPen(pen) 

        rect = event.rect()
        painter.fillRect(rect, self.color)

        painter.end()