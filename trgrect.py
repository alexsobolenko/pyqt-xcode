#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter, QColor
from PyQt5.QtCore import QRectF, Qt

from fontloader import FontLoader

class TrgRect(QGraphicsObject):
	size 	= 1
	h 		= 1
	value 	= 1
	row 	= 1
	col 	= 1
	penWidth = 1

	def __init__(self, parent):
		super().__init__()

		clr0 = QColor(255, 160, 122)
		clr1 = QColor(240, 230, 140)
		clr2 = QColor(135, 206, 250)
		clr3 = QColor(210, 105, 30)
		clr4 = QColor(0, 255, 127)
		clr5 = QColor(0, 139, 139)
		self.color = [clr0, clr1, clr2, clr3, clr4, clr5]

	def boundingRect(self):
		return QRectF(self.posx, self.posy, self.size, self.size)

	def paint(self, painter, option, widget):
		rec = self.boundingRect()
		self.pen = QPen(Qt.black, self.penWidth)
		font = painter.font()
		font.setPointSize(int(self.size/2.2))
		painter.setFont(font)
		painter.setBrush(QBrush(self.color[self.value]))
		painter.setPen(self.pen)
		painter.fillRect(rec, QBrush(self.color[self.value]))
		painter.drawRoundedRect(rec, 2.0, 2.0)
		painter.drawText(rec, Qt.AlignCenter, str(self.value))

	def setGeometry(self, row, col):
		self.row = row
		self.col = col
		self.posx = self.col*self.size + (self.col + 4)*self.h
		self.posy = (self.row + (2/3))*self.size + (self.row + 8)*self.h 
		self.update()

	def setSize(self, size, h):
		self.size = size
		self.h = h
		self.update()

	def setValue(self, value):
		self.value = value
		self.update()

	def setPenWidth(self, w):
		self.penWidth = w
		self.update()