from PyQt5.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter, QColor, QImage
from PyQt5.QtCore import QRectF, Qt, pyqtSignal, QSize
from fontloader import FontLoader

class MenuRect(QGraphicsObject):
    width = 1
    height = 1
    posx = 1
    posy = 1
    penWidth = 1
    pressed = False
    img = -1
    clickable = True
    hoverEnter = pyqtSignal()
    hoverExit = pyqtSignal()
    clicked = pyqtSignal()


    def __init__(self, parent, img, cl = True):
        super().__init__()

        self.img = img
        self.clickable = cl

        if cl:
            self.co = 0
        else:
            self.co = 1

        clr0 = QColor(255, 160, 122)
        clr1 = QColor(240, 230, 140)
        clr2 = QColor(135, 206, 250)
        clr3 = QColor(210, 105, 30)
        clr4 = QColor(0, 255, 127)

        self.color = [clr0, clr1, clr2, clr3, clr4]
        self.setAcceptHoverEvents(True)


    def boundingRect(self):
        return QRectF(self.posx, self.posy, self.width, self.height)


    def paint(self, painter, option, widget):
        rec = self.boundingRect()
        self.pen = QPen(Qt.black, self.penWidth)
        font = painter.font()
        font.setFamily('Century Gothic')
        font.setPointSize(int(self.height/3.3))

        painter.setFont(font)
        painter.setBrush(QBrush(self.color[self.co]))
        painter.setPen(self.pen)
        painter.fillRect(rec, QBrush(self.color[0]))
        painter.drawRoundedRect(rec, 2.0, 2.0)
        painter.drawText(rec, Qt.AlignCenter, self.img)


    def setGeometry(self, x, y):
        self.posx = x
        self.posy = y
        self.update()


    def setSize(self, w, h):
        self.width = w
        self.height = h
        self.update()


    def setPenWidth(self, w):
        self.penWidth = w
        self.update()


    def setText(self, text):
        self.img = str(text)
        self.update()


    def hoverEnterEvent(self, event):
        if self.clickable:
            self.hoverEnter.emit()


    def hoverLeaveEvent(self, event):
        if self.clickable:
            self.hoverExit.emit()


    def mousePressEvent(self, event):
        if self.clickable:
            pressed = True


    def mouseReleaseEvent(self, event):
        if self.clickable:
            pressed = False
            self.clicked.emit()
