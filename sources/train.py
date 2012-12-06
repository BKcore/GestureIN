#!/usr/bin/python

import sys
import cv2
import cv
import numpy as np

from PyQt4 import QtGui
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
(options, args) = parser.parse_args()

app 	= QtGui.QApplication(sys.argv)
window 	= QtGui.QMainWindow()
canvas 	= QtGui.QGraphicsScene()
view 	= QtGui.QGraphicsView(canvas, window)
img 	= QtGui.QImage(options.filename)
pixmap 	= QtGui.QPixmap.fromImage(img)

view.resize(202, 202)
window.resize(800, 600)
canvas.addPixmap(pixmap)


window.show()
sys.exit(app.exec_())