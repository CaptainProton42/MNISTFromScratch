from PyQt5 import QtGui, QtCore, QtWidgets

class Bar(QtWidgets.QFrame):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        
        self.color = QtGui.QColor()
        self.color.setNamedColor("steelblue")
        self.textColor = QtGui.QColor()
        self.textColor.setNamedColor("black")
        self.value = 0.0

    def setValue(self, value):
        # clamp between 0.0 and 1.0
        self.value = max(min(value, 1.0), 0.0)
        self.repaint()

    def setColor(self, color):
        self.color = color

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)     

        rect_pen = QtGui.QPen(self.color)
        text_pen = QtGui.QPen(self.textColor)

        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        rect = event.rect()
        rect.setHeight(self.value * event.rect().height())
        rect.moveBottom(event.rect().bottom())

        painter.setPen(rect_pen) 
        painter.fillRect(rect, self.color)

        painter.setPen(text_pen)
        painter.drawText(event.rect(), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, "%.0f %%" % (100 * self.value))

        painter.end()