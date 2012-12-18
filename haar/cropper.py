#!/usr/bin/python

import sys
import os

from optparse import OptionParser
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class CropperViewer(QWidget):

	def __init__(self, fichiers = []):
		QObject.__init__(self)

		self.currentImage = 0
		self.cropRectangle = [[0, 0], 50]
		self.fichiers = fichiers
		self.fastMove = False

		self.original = QLabel()
		self.original.setFixedHeight(200)
		self.original.setFixedWidth(200)
		self.original.setScaledContents(True)

		self.crop = QLabel()
		self.crop.setFixedHeight(200)
		self.crop.setFixedWidth(200)
		self.crop.setScaledContents(True)

		layout = QHBoxLayout()
		layout.addWidget(self.original)
		layout.addWidget(self.crop)

		self.setLayout(layout)

		self.setFocusPolicy(Qt.StrongFocus)
		self.setFocus()

		if len(self.fichiers) > 0:
			self.loadImage()

	def nextImage(self):
		if self.currentImage == len(self.fichiers) - 1:
			self.currentImage = 0
		else:
			self.currentImage += 1

		self.loadImage()

	def loadImage(self):
		fichier = self.fichiers[self.currentImage]
		original_pixmap = QPixmap(fichier)
		painter = QPainter(original_pixmap)
		pen = QPen(Qt.red, 1, Qt.SolidLine)

		self.crop.setPixmap(original_pixmap.copy(self.cropRectangle[0][0], self.cropRectangle[0][1], self.cropRectangle[1], self.cropRectangle[1]))

		painter.setPen(pen)
		painter.drawRect(self.cropRectangle[0][0], self.cropRectangle[0][1], self.cropRectangle[1], self.cropRectangle[1])

		self.original.setPixmap(original_pixmap)

		painter.end()

	def keyPressEvent(self, event):
		if self.fastMove:
			move = 10
		else:
			move = 1

		if event.key() == Qt.Key_Right:
			if self.cropRectangle[0][0] < 200 - move - self.cropRectangle[1]:
				self.cropRectangle[0][0] += move
				self.loadImage()
		elif event.key() == Qt.Key_Left:
			if self.cropRectangle[0][0] >= move:
				self.cropRectangle[0][0] -= move
				self.loadImage()
		elif event.key() == Qt.Key_Up:
			if self.cropRectangle[0][1] >= move:
				self.cropRectangle[0][1] -= move
				self.loadImage()
		elif event.key() == Qt.Key_Down:
			if self.cropRectangle[0][1] < 200 - move - self.cropRectangle[1]:
				self.cropRectangle[0][1] += move
				self.loadImage()
		elif event.key() == Qt.Key_S:
			if self.cropRectangle[1] <= 200 - move:
				self.cropRectangle[1] += move
				self.loadImage()
		elif event.key() == Qt.Key_Z:
			if self.cropRectangle[1] >= move + 1:
				self.cropRectangle[1] -= move
				self.loadImage()
		elif event.key() == Qt.Key_Return:
			self.crop.pixmap().save(self.fichiers[self.currentImage], "png")
			self.nextImage()
		elif event.key() == Qt.Key_Space:
			self.nextImage()
		elif event.key() == Qt.Key_Control:
			self.fastMove = True
		else:
			QWidget.keyPressEvent(self, event)

	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Control:
			self.fastMove = False

if __name__ == '__main__' :
	parser = OptionParser()
	parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
	(options, args) = parser.parse_args()

	fichiers = []

	for root, dirs, files in os.walk(options.dirname):
		for i in files:
			fichiers.append(os.path.join(root, i))

	fichiers.sort(key=lambda x: os.path.basename(x))

	app = QApplication(sys.argv)

	cropper_viewer = CropperViewer(fichiers)
	cropper_viewer.show()

	sys.exit(app.exec_())