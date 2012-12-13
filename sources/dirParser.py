#!/usr/bin/python

import sys
import cv2
import cv
import numpy as np

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from optparse import OptionParser
import os.path

import detect

class Viewer (QObject):
    def __init__(self):
        QObject.__init__(self)
        self.currentIm = 0
        self.fichier = []
        self.length = 0
        self.original = QLabel()
        self.transform1 = QLabel()
        self.transform2 = QLabel()
        self.doPlay = False
        self.startTimer(1000/12)

    def timerEvent(self,e):
        if(self.doPlay):
            self.nextImage()

    def listDirectory(self, path): 
        
        for root, dirs, files in os.walk(path): 
            for i in files: 
                self.fichier.append(os.path.join(root, i)) 

        self.fichier.sort(key=lambda x: os.path.basename(x))
        self.length = len(self.fichier)
        return self.fichier

    def nextImage(self):
        if(self.currentIm == self.length):
            self.currentIm = 0
        else:
            self.currentIm = self.currentIm+1

        self.setCurrentIm(self.currentIm)

    def previousImage(self):
        if(self.currentIm == 0):
            self.currentIm = self.length
        else:
            self.currentIm = self.currentIm -1

        self.setCurrentIm(self.currentIm)


    def setCurrentIm(self,ind):
        self.original.setPixmap(QPixmap(self.fichier[ind]))
        img1,img2 = detect.loadAndProcess(self.fichier[ind])
        width = img1.shape[1]
        height = img1.shape[0]
        self.transform1.setPixmap(QPixmap.fromImage(QImage(img1.tostring(),width,height,QImage.Format_RGB888)))
        self.transform2.setPixmap(QPixmap.fromImage(QImage(img2.tostring(),width,height,QImage.Format_RGB888)))
        return

    def play(self):
        self.doPlay = not self.doPlay


if __name__ == '__main__' :
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
    (options, args) = parser.parse_args()

    app=QApplication(sys.argv)

    v = Viewer()

    v.listDirectory(options.dirname)

    v.setCurrentIm(0)

    window = QWidget()
    hLayout = QHBoxLayout()
    vLayout = QVBoxLayout()
    buttonLayout = QHBoxLayout()

    exitButton = QPushButton("Exit",window)
    playButton = QPushButton("Play",window)
    previous = QPushButton("",window)
    next = QPushButton("",window)

    previous.setIcon(QIcon.fromTheme("go-previous"))
    next.setIcon(QIcon.fromTheme("go-next"))
    exitButton.setIcon(QIcon.fromTheme("application-exit"))
    playButton.setIcon(QIcon.fromTheme("media-playback-start"))


    hLayout.addWidget(previous)
    hLayout.addWidget(v.original)
    hLayout.addWidget(v.transform1)
    hLayout.addWidget(v.transform2)
    hLayout.addWidget(next)

    buttonLayout.addWidget(playButton)
    buttonLayout.addWidget(exitButton)

    vLayout.addLayout(hLayout)
    vLayout.addLayout(buttonLayout)

    window.setLayout(vLayout)


    QObject.connect(exitButton,SIGNAL("clicked()"),app.exit)
    QObject.connect(previous,SIGNAL("clicked()"),v.previousImage)
    QObject.connect(next,SIGNAL("clicked()"),v.nextImage)
    QObject.connect(playButton,SIGNAL("clicked()"),v.play)
     
    window.show()
    sys.exit(app.exec_())