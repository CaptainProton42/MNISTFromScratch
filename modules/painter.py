from PyQt5 import QtGui, QtCore, QtWidgets

# This class represents a single point with x and y coordinates.
class Point:
    x = 0
    y = 0

    # Constructor
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Setter
    def setCoords(self, x, y):
        self.x = x
        self.y = y

# Holds information about a point in the drawing
class Shape:
    location = Point(0, 0)
    index = 0

    # Constructor
    def __init__(self, location, index):
        self.location = location
        self.index = index

# Holds information about the drawing as whole, combining multiple Shapes
class Shapes:
    # Stores all the shapes
    __Shapes = []

    # Constructor
    def __init__(self):
        self.__Shapes = []

    # Returns the number of shapes being stored.
    def getNumberOfShapes(self):
        return len(self.__Shapes)

    # Add a shape to the database, recording its position,
    # width, colour and shape relation information
    def addShape(self, location, index):
        shape = Shape(location, index)
        self.__Shapes.append(shape)

    # returns the shape at the requested index.
    def getShape(self, index):
        return self.__Shapes[index]

    # Removes any point data within a certain threshold of a point.
    def removeShapeAtLoc(self, location, threshold):
        # while True is neccessary so the list size can change in the loop
        i = 0
        while True:
            if(i==len(self.__Shapes)):
                break 
            # finds if a point is within a certain distance of the point to remove.
            if((abs(location.x - self.__Shapes[i].location.x) < threshold) and (abs(location.y - self.__Shapes[i].location.y) < threshold)):
                # removes all data for that index
                del self.__Shapes[i]

                # goes through the rest of the data and adds an extra
                # 1 to defined them as a seprate shape and shuffles on the effect.
                for n in range(len(self.__Shapes)-i):
                    self.__Shapes[n+i].index += 1
                # Go back a step so we dont miss a point.
                i -= 1
            i += 1

class Painter(QtWidgets.QFrame):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        self.isPainting = False
        self.shapeNum = 0

        self.img = QtGui.QImage()
        self.imgActive = False

        self.mouseLoc = Point(0,0)  
        self.lastPos = Point(0,0)  
        self.drawingShapes = Shapes()
        self.mouseLoc = Point(0,0)
        self.lastPos = Point(0,0)
        
    def clearCanvas(self):
        self.drawingShapes = Shapes()
        self.shapeNum = 0
        self.imgActive = False
        self.repaint()

    #Mouse down event
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.isPainting = True
            self.lastPos = Point(event.x(), event.y())
            self.shapeNum += 1
            self.drawingShapes.addShape(self.lastPos, self.shapeNum)
            self.imgActive = False
            self.repaint()
        elif event.button() == QtCore.Qt.RightButton:
            self.clearCanvas()

    #Mouse Move event
    def mouseMoveEvent(self, event):
        if (self.isPainting == True):
            self.mouseLoc = Point(event.x(), event.y())
            if (self.lastPos.x != self.mouseLoc.x) or (self.lastPos.y != self.mouseLoc.y):
                self.lastPos = Point(event.x(), event.y())
                self.drawingShapes.addShape(self.lastPos, self.shapeNum)
            self.repaint()

    #Mose Up Event
    def mouseReleaseEvent(self, event):
        if(self.isPainting == True):
            self.isPainting = False

    def drawLines(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)     

        pen = QtGui.QPen(QtGui.QColor(0.0 ,0.0 ,0.0), 25.0, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap)
        painter.setPen(pen) 

        for i in range(self.drawingShapes.getNumberOfShapes()):
            T1 = self.drawingShapes.getShape(i)

            painter.drawPoint(T1.location.x, T1.location.y)

            if (i > 0):
                T = self.drawingShapes.getShape(i-1)

                if (T.index == T1.index):
                    painter.drawLine(T.location.x,T.location.y,T1.location.x,T1.location.y)

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawLines(painter)
        if (self.imgActive):
            rect = self.geometry()
            rect.moveTopLeft(QtCore.QPoint(0, 0))
            painter.drawImage(rect, self.img)
        painter.end()

    def showImage(self, img):
        self.imgActive = True
        self.img = img
        self.repaint()