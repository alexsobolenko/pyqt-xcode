#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, qApp
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsObject, QStyleOptionGraphicsItem
from PyQt5.QtCore import QRectF, Qt, QSize
from PyQt5.QtGui import QBrush, QPen, QFont, QPainter

from gamerect import GameRect
from trgrect  import TrgRect
from menurect import MenuRect


class XCode(QWidget):
	def __init__(self):
		super().__init__()

		self.games = 0
		self.wins = 0
		self.dif = 0
		self.lang = 0

		# размеры окна
		self.ms 		= QSize(480, 854)

		# рамеры промежутков, кнопок и сетки
		self.h 			= int(((self.ms.width()/100) + (self.ms.height()/200))/2)
		s1 				= int((3*(self.ms.height() - 24*self.h))/32) - 1
		s2 				= int((self.ms.width() - 12*self.h))
		if s1 > s2:
			self.size 	= s2
		else:
			self.size 	= s1
		self.net 		= 5

		# пустые массивы кнопок
		self.rect 		= []
		self.trg 		= []

		# основные элементы графики
		self.view 		= QGraphicsView()
		self.menuScene 	= QGraphicsScene()
		self.gameScene 	= QGraphicsScene()
		self.toolsScene = QGraphicsScene()
		self.helpScene 	= QGraphicsScene()

		# заголовок
		label = MenuRect(self, 'xCode', False)
		label.setSize(self.ms.width() - 8*self.h, self.size*2)
		label.setGeometry(4*self.h, self.ms.height()/3)
		self.menuScene.addItem(label)

		# кнопка перехода на экран игры
		btnPlay = MenuRect(self, 'play')
		btnPlay.setSize((self.ms.width() - 11*self.h)/4, (self.ms.width() - 11*self.h)/4)
		btnPlay.setGeometry(4*self.h, self.ms.height()/3 + 2*self.size + 2*self.h)
		btnPlay.hoverEnter.connect(lambda: btnPlay.setPenWidth(4))
		btnPlay.hoverExit.connect(lambda: btnPlay.setPenWidth(1))
		btnPlay.clicked.connect(lambda: self.view.setScene(self.gameScene))
		self.menuScene.addItem(btnPlay)

		# кнопка перехода на экран настроек
		btnTools = MenuRect(self, 'tools')
		btnTools.setSize((self.ms.width() - 11*self.h)/4, (self.ms.width() - 11*self.h)/4)
		btnTools.setGeometry(self.h*5 + (self.ms.width() - 11*self.h)/4, self.ms.height()/3 + 2*self.size + 2*self.h)
		btnTools.hoverEnter.connect(lambda: btnTools.setPenWidth(4))
		btnTools.hoverExit.connect(lambda: btnTools.setPenWidth(1))
		btnTools.clicked.connect(lambda: self.view.setScene(self.toolsScene))
		self.menuScene.addItem(btnTools)

		# кнопка перехода на экран помощи
		btnHelp = MenuRect(self, 'help')
		btnHelp.setSize((self.ms.width() - 11*self.h)/4, (self.ms.width() - 11*self.h)/4)
		btnHelp.setGeometry(self.h*6 + (self.ms.width() - 11*self.h)/2, self.ms.height()/3 + 2*self.size + 2*self.h)
		btnHelp.hoverEnter.connect(lambda: btnHelp.setPenWidth(4))
		btnHelp.hoverExit.connect(lambda: btnHelp.setPenWidth(1))
		btnHelp.clicked.connect(lambda: self.view.setScene(self.helpScene))
		self.menuScene.addItem(btnHelp)

		# кнопка завершения работы
		btnExit = MenuRect(self, 'exit')
		btnExit.setSize((self.ms.width() - 11*self.h)/4, (self.ms.width() - 11*self.h)/4)
		btnExit.setGeometry(self.h*7 + 3*(self.ms.width() - 11*self.h)/4, self.ms.height()/3 + 2*self.size + 2*self.h)
		btnExit.hoverEnter.connect(lambda: btnExit.setPenWidth(4))
		btnExit.hoverExit.connect(lambda: btnExit.setPenWidth(1))
		btnExit.clicked.connect(lambda: qApp.quit())
		self.menuScene.addItem(btnExit)

		# по умолчанию запускается экран главного меню
		self.view.setScene(self.menuScene)

		# настройка экрана игры
		# кнопка возврата в главное меню
		btnMenu = MenuRect(self, 'menu')
		btnMenu.setSize(2*self.size/3, 2*self.size/3)
		btnMenu.setGeometry(4*self.h, 4*self.h)
		btnMenu.hoverEnter.connect(lambda: btnMenu.setPenWidth(4))
		btnMenu.hoverExit.connect(lambda: btnMenu.setPenWidth(1))
		btnMenu.clicked.connect(lambda: self.view.setScene(self.menuScene))
		self.gameScene.addItem(btnMenu)

		# табло со статистикой игры
		self.tableText = 'games: ' + str(self.games) + ' wins: ' + str(self.wins)
		self.table = MenuRect(self, self.tableText, False)
		self.table.setSize(self.size*3 + self.h, 2*self.size/3)
		self.table.setGeometry(5*self.h + 2*self.size/3, 4*self.h)
		self.gameScene.addItem(self.table)

		# кнопка начала новой игры
		btnNewGame = MenuRect(self, 'new\ngame')
		btnNewGame.setSize(2*self.size/3, 2*self.size/3)
		btnNewGame.setGeometry(11*self.size/3 + self.h*7, 4*self.h)
		btnNewGame.clicked.connect(lambda: self.newGame())
		btnNewGame.hoverEnter.connect(lambda: btnNewGame.setPenWidth(4))
		btnNewGame.hoverExit.connect(lambda: btnNewGame.setPenWidth(1))
		self.gameScene.addItem(btnNewGame)

		# кнопка перезапуска текущей игры
		btnRestart = MenuRect(self, 'restart')
		btnRestart.setSize(2*self.size/3, 2*self.size/3)
		btnRestart.setGeometry(13*self.size/3 + self.h*8, 4*self.h)
		btnRestart.clicked.connect(lambda: self.restart())
		btnRestart.hoverEnter.connect(lambda: btnRestart.setPenWidth(4))
		btnRestart.hoverExit.connect(lambda: btnRestart.setPenWidth(1))
		self.gameScene.addItem(btnRestart)

		# поле задачи
		for i in range(self.net):
			for j in range(self.net):
				r = TrgRect(self)
				r.setSize(self.size, self.h)
				r.setValue(0)
				r.setGeometry(i, j)
				self.trg.append(r)
				self.gameScene.addItem(r)

		# поле игровых кнопок
		for i in range(self.net):
			for j in range(self.net):
				r = GameRect(self)
				r.setSize(self.size, self.h)
				r.setValue(0)
				r.setGeometry(i, j)
				r.hoverEnter.connect(lambda: self.hoverChange(4))
				r.hoverExit.connect(lambda: self.hoverChange(1))
				r.clicked.connect(lambda: self.click())
				self.rect.append(r)
				self.gameScene.addItem(r)

		# настройка экрана настроек
		# заголовок
		labelTools = MenuRect(self, 'Tools', False)
		labelTools.setSize(self.ms.width() - 8*self.h, self.size)
		labelTools.setGeometry(4*self.h, 4*self.h)
		self.toolsScene.addItem(labelTools)

		# заголовок выбора сложности
		labelDif = MenuRect(self, 'Difficulty', False)
		labelDif.setSize(self.ms.width() - 8*self.h, self.size)
		labelDif.setGeometry(4*self.h, 12*self.h + self.size)
		self.toolsScene.addItem(labelDif)

		# заголовок отображает уровень сложности
		self.btnDifText = ['Easy', 'Normal', 'Hard']
		self.btnDif = MenuRect(self, self.btnDifText[self.dif], False)
		self.btnDif.setSize(self.ms.width() - 2*self.size - 12*self.h, self.size)
		self.btnDif.setGeometry(6*self.h + self.size, 16*self.h + 2*self.size)
		self.toolsScene.addItem(self.btnDif)

		#кнопки изменения уровня сложности
		btnDifM = MenuRect(self, '<')
		btnDifM.setSize(self.size, self.size)
		btnDifM.setGeometry(4*self.h, 16*self.h + 2*self.size)
		btnDifM.clicked.connect(lambda: self.changeDifficulty(False))
		btnDifM.hoverEnter.connect(lambda: btnDifM.setPenWidth(4))
		btnDifM.hoverExit.connect(lambda: btnDifM.setPenWidth(1))
		self.toolsScene.addItem(btnDifM)
		btnDifP = MenuRect(self, '>')
		btnDifP.setSize(self.size, self.size)
		btnDifP.setGeometry(self.ms.width() - 4*self.h - self.size, 16*self.h + 2*self.size)
		btnDifP.clicked.connect(lambda: self.changeDifficulty(True))
		btnDifP.hoverEnter.connect(lambda: btnDifP.setPenWidth(4))
		btnDifP.hoverExit.connect(lambda: btnDifP.setPenWidth(1))
		self.toolsScene.addItem(btnDifP)

		# заголовок выбора языка
		labelLang = MenuRect(self, 'Language', False)
		labelLang.setSize(self.ms.width() - 8*self.h, self.size)
		labelLang.setGeometry(4*self.h, 20*self.h + 3*self.size)
		self.toolsScene.addItem(labelLang)

		# заголовок отображает язык
		self.btnLangText = ['RUS', 'ENG']
		self.btnLang = MenuRect(self, self.btnLangText[self.lang], False)
		self.btnLang.setSize(self.ms.width() - 2*self.size - 12*self.h, self.size)
		self.btnLang.setGeometry(6*self.h + self.size, 24*self.h + 4*self.size)
		self.toolsScene.addItem(self.btnLang)

		#кнопки изменения языка
		btnLangM = MenuRect(self, '<')
		btnLangM.setSize(self.size, self.size)
		btnLangM.setGeometry(4*self.h, 24*self.h + 4*self.size)
		btnLangM.clicked.connect(lambda: self.changeLanguage())
		btnLangM.hoverEnter.connect(lambda: btnLangM.setPenWidth(4))
		btnLangM.hoverExit.connect(lambda: btnLangM.setPenWidth(1))
		self.toolsScene.addItem(btnLangM)
		btnLangP = MenuRect(self, '>')
		btnLangP.setSize(self.size, self.size)
		btnLangP.setGeometry(self.ms.width() - 4*self.h - self.size, 24*self.h + 4*self.size)
		btnLangP.clicked.connect(lambda: self.changeLanguage())
		btnLangP.hoverEnter.connect(lambda: btnLangP.setPenWidth(4))
		btnLangP.hoverExit.connect(lambda: btnLangP.setPenWidth(1))
		self.toolsScene.addItem(btnLangP)

		# заголовок сброса настроек
		self.labelClear = MenuRect(self, self.tableText, False)
		self.labelClear.setSize(self.ms.width() - 8*self.h, self.size)
		self.labelClear.setGeometry(4*self.h, 28*self.h + 5*self.size)
		self.toolsScene.addItem(self.labelClear)

		# кнопка сброса настроек
		btnClear = MenuRect(self, 'Clear stats')
		btnClear.setSize(self.ms.width() - 8*self.h, self.size)
		btnClear.setGeometry(4*self.h, 32*self.h + 6*self.size)
		btnClear.clicked.connect(lambda: self.clearStats())
		btnClear.hoverEnter.connect(lambda: btnClear.setPenWidth(4))
		btnClear.hoverExit.connect(lambda: btnClear.setPenWidth(1))
		self.toolsScene.addItem(btnClear)

		# кнопка применения настроек
		btnToolsOk = MenuRect(self, 'OK')
		btnToolsOk.setSize((self.ms.width() - 10*self.h)/2, self.size)
		btnToolsOk.setGeometry(4*self.h, self.ms.height() - self.size - 4*self.h)
		btnToolsOk.clicked.connect(lambda: self.confirmChanges(True))
		btnToolsOk.hoverEnter.connect(lambda: btnToolsOk.setPenWidth(4))
		btnToolsOk.hoverExit.connect(lambda: btnToolsOk.setPenWidth(1))
		self.toolsScene.addItem(btnToolsOk)

		# кнопка отказа от применения настроек
		btnToolsCancel = MenuRect(self, 'Cancel')
		btnToolsCancel.setSize((self.ms.width() - 10*self.h)/2, self.size)
		btnToolsCancel.setGeometry((self.ms.width() + 2*self.h)/2, self.ms.height() - self.size - 4*self.h)
		btnToolsCancel.clicked.connect(lambda: self.confirmChanges(False))
		btnToolsCancel.hoverEnter.connect(lambda: btnToolsCancel.setPenWidth(4))
		btnToolsCancel.hoverExit.connect(lambda: btnToolsCancel.setPenWidth(1))
		self.toolsScene.addItem(btnToolsCancel)

		# настройка экрана помощи
		# заголовок
		labelHelp = MenuRect(self, 'Help', False)
		labelHelp.setSize(self.ms.width() - 8*self.h, self.size)
		labelHelp.setGeometry(4*self.h, 4*self.h)
		self.helpScene.addItem(labelHelp)

		# кнопка возврата в меню
		btnHelpMenu = MenuRect(self, 'Menu')
		btnHelpMenu.setSize(self.ms.width() - 8*self.h, self.size)
		btnHelpMenu.setGeometry(4*self.h, self.ms.height() - self.size - 4*self.h)
		btnHelpMenu.clicked.connect(lambda: self.view.setScene(self.menuScene))
		btnHelpMenu.hoverEnter.connect(lambda: btnHelpMenu.setPenWidth(4))
		btnHelpMenu.hoverExit.connect(lambda: btnHelpMenu.setPenWidth(1))
		self.helpScene.addItem(btnHelpMenu)

		# новая игра
		self.newGame()

		# установка фиксированного размера и запуск виджета
		self.view.setFixedSize(self.ms)
		self.view.show()

	def clearStats(self):
		self.games, self.wins = 0, 0
		self.setTableText()

	def setTableText(self):
		self.tableText = 'games: ' + str(self.games) + ' wins: ' + str(self.wins)
		self.table.setText(self.tableText)
		self.labelClear.setText(self.tableText)

	def changeDifficulty(self, up):
		if up:
			self.dif += 1
			if self.dif == 3:
				self.dif = 0
		else:
			self.dif -= 1
			if self.dif == -1:
				self.dif = 2
		self.btnDif.setText(self.btnDifText[self.dif])

	def changeLanguage(self):
		ll = {0:1, 1:0}
		self.lang = int(ll[self.lang])
		self.btnLang.setText(self.btnLangText[self.lang])


	def confirmChanges(self, confirm):
		if confirm:
			pass
		self.view.setScene(self.menuScene)

	# перезапуск текущей игры
	def restart(self):	
		# обнуление игровых кнопок	
		for i in range(self.net*self.net):
			self.rect[i].setValue(0)

	# начало новой игры
	def newGame(self):
		self.games += 1
		self.setTableText()

		# обнуление игровых кнопок и кнопок задачи
		for i in range(self.net*self.net):
			self.rect[i].setValue(0)
			self.trg[i].setValue(0)

		# составление задачи
		i = 0
		k = random.randint(12, 18)
		while i < k:
			row = random.randint(0, self.net - 1)
			col = random.randint(0, self.net - 1)
			if self.trg[row*self.net + col].value == 0:
				i += 1
				self.trg[row*self.net + col].setValue(1)
				if row > 0:
					if self.trg[(row - 1)*self.net + col].value != 0:
						self.trg[(row - 1)*self.net + col].setValue(self.trg[(row - 1)*self.net + col].value + 1)
				if row < (self.net - 1):
					if self.trg[(row + 1)*self.net + col].value != 0:
						self.trg[(row + 1)*self.net + col].setValue(self.trg[(row + 1)*self.net + col].value + 1)
				if col > 0:
					if self.trg[row*self.net + col - 1].value != 0:
						self.trg[row*self.net + col - 1].setValue(self.trg[row*self.net + col - 1].value + 1)
				if col < (self.net - 1):
					if self.trg[row*self.net + col + 1].value != 0:
						self.trg[row*self.net + col + 1].setValue(self.trg[row*self.net + col + 1].value + 1)

	# выделение жирной границей кнопок при наведении на них мыши
	def hoverChange(self, w):
		rec = self.sender()
		row, col = rec.getCoord()
		self.rect[row*self.net + col].setPenWidth(w)
		self.trg[row*self.net + col].setPenWidth(w)

	# реакция на нажатие на игровую кнопку
	def click(self):		
		rec = self.sender()
		row, col = rec.getCoord()
		if rec.value == 0:
			rec.setValue(1)
			#if row > 0:
			#	if self.rect[(row - 1)*self.net + col].value != 0:
			#		self.rect[(row - 1)*self.net + col].setValue(self.rect[(row - 1)*self.net + col].value + 1)
			#if row < (self.net - 1):
			#	if self.rect[(row + 1)*self.net + col].value != 0:
			#		self.rect[(row + 1)*self.net + col].setValue(self.rect[(row + 1)*self.net + col].value + 1)
			#if col > 0:
			#	if self.rect[row*self.net + col - 1].value != 0:
			#		self.rect[row*self.net + col - 1].setValue(self.rect[row*self.net + col - 1].value + 1)
			#if col < (self.net - 1):
			#	if self.rect[row*self.net + col + 1].value != 0:
			#		self.rect[row*self.net + col + 1].setValue(self.rect[row*self.net + col + 1].value + 1)
			self.addNeighbour((row - 1)*self.net + col, (row > 0))
			self.addNeighbour((row + 1)*self.net + col, (row < (self.net - 1)))
			self.addNeighbour(row*self.net + col - 1, (col > 0))
			self.addNeighbour(row*self.net + col + 1, (col < (self.net - 1)))


	def addNeighbour(self, cell, uslov):
		if uslov:
			if self.rect[cell].value != 0:
				self.rect[cell].setValue(self.rect[cell].value + 1)

		# проверка на завершение игры победой
		x = 0
		for i in range(self.net*self.net):
			if self.rect[i].value != self.trg[i].value:
				x += 1
		if x == 0:
			print(self.wins)
			self.wins += 1
			print(self.wins)
			self.setTableText()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = XCode()
	sys.exit(app.exec_())
