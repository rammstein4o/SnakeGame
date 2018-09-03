from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QBrush, QPen

class Field(QWidget):

    def __init__(self, config, x, y, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self.config = config
        self.resolution = int(self.config['ui']['resolution'])
        self.setFixedSize(QSize(self.resolution, self.resolution))
        self.x = x
        self.y = y
        self.isHead = False
        self.isSnake = False
        self.isApple = False

    def reset(self):
        self.isHead = False
        self.isSnake = False
        self.isApple = False
        self.update()

    def setHead(self):
        self.isHead = True
        self.isSnake = False
        self.isApple = False
        self.update()

    def setSnake(self):
        self.isHead = False
        self.isSnake = True
        self.isApple = False
        self.update()
    
    def setApple(self):
        self.isHead = False
        self.isSnake = False
        self.isApple = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rectangle = event.rect()
        
        if self.isHead:
            color = Qt.darkYellow
        elif self.isSnake:
            color = Qt.darkGreen
        elif self.isApple:
            color = Qt.darkRed
        else:
            color = Qt.lightGray
        
        painter.fillRect(rectangle, QBrush(color))
        pen = QPen(color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(rectangle)
