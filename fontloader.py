from PyQt5.QtCore import QIODevice, QByteArray, QFile
from PyQt5.QtGui import QFontDatabase, QFont

class FontLoader(QFont):
	def __init__(self, parent, fileName, pointSize):
		super().__init__()

		file = QFile(fileName + '.ttf')
		file.open(QIODevice.ReadOnly)
		fontData = QByteArray(file.readAll())
		dbFont = QFontDatabase()
		idFont = dbFont.addApplicationFontFromData(fontData)
		fontFamily = dbFont.applicationFontFamilies(idFont)[0]
		#font = QFont(fontFamily)
		self.setFamily(fontFamily)
		self.setPointSize(pointSize)