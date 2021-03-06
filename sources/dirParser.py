#!/usr/bin/python

import os
import sys
import cv2
import cv
import numpy as np

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from optparse import OptionParser
import os.path

import io,json

import detect
import haar

class Viewer (QObject):
    haarClassifier = haar.haarInit(os.path.dirname(os.path.realpath(__file__)) + '/../haar/cascade.xml')

    def __init__(self):
        QObject.__init__(self)
        self.currentIm = 0
        self.fichier = []
        self.currentDir = ""
        self.length = 0
        self.original = QLabel()
        self.transform1 = QLabel()
        self.transform2 = QLabel()
        self.fileName = QLabel()
        self.fileName.setAlignment(Qt.AlignHCenter)
        self.fileClass = QLabel()
        self.fileClass.setAlignment(Qt.AlignHCenter)
        self.prediction = QLabel()
        self.classifier = cv2.NormalBayesClassifier()
        self.classifier.load(os.path.dirname(os.path.realpath(__file__)) + '/../bayes/bayes.xml')
        self.dictionary = dict()
        self.doPlay = False
        self.startTimer(1000/12)

    def timerEvent(self,e):
        if(self.doPlay):
            self.nextImage()

    def listDirectory(self, path): 
        
        self.currentDir = path
        for root, dirs, files in os.walk(path): 
            for i in files: 
                self.fichier.append(os.path.join(root, i)) 

        self.fichier.sort(key=lambda x: os.path.basename(x))
        self.length = len(self.fichier)
        return self.fichier

    def nextImage(self):
        if(self.currentIm == self.length-1):
            self.currentIm = 0
        else:
            self.currentIm = self.currentIm+1

        self.setCurrentIm(self.currentIm)

    def previousImage(self):
        if(self.currentIm == 0):
            self.currentIm = self.length-1
        else:
            self.currentIm = self.currentIm -1

        self.setCurrentIm(self.currentIm)



    def setCurrentIm(self,ind):
        self.original.setPixmap(QPixmap(self.fichier[ind]))

        img1,img2,density= detect.loadAndProcess(self.fichier[ind], self.haarClassifier)

        if density is None:

            self.prediction.setText('Pas de main')
            
        else:

            sample = np.matrix(density).astype('float32')
            _,result = self.classifier.predict(sample)

            bayesResult = int(result[[0]])

            if(bayesResult == -1):
                self.prediction.setText("Pas de main")
            elif(bayesResult == 0):
                self.prediction.setText("Poing")
            elif(bayesResult==1):
                self.prediction.setText("1 doigt")
            elif(bayesResult==2):
                self.prediction.setText("2 doigts")
            elif(bayesResult==3):
                self.prediction.setText("3 doigts")
            elif(bayesResult==4):
                self.prediction.setText("4 doigts")
            elif(bayesResult==5):
                self.prediction.setText("5 doigts")

        
        width = img1.shape[1]
        height = img1.shape[0]

        pix1 = QPixmap.fromImage(QImage(img1.tostring(),width,height,QImage.Format_RGB888))
        pix2 = QPixmap.fromImage(QImage(img2.tostring(),width,height,QImage.Format_RGB888))

        self.transform1.setPixmap(pix1)
        self.transform1.setFixedSize(pix1.size())
        self.transform2.setPixmap(pix2)
        self.transform2.setFixedSize(pix2.size())

        self.fileName.setText(self.fichier[ind])
        if(self.fichier[ind] in self.dictionary):
            self.fileClass.setText(str(self.dictionary[self.fichier[ind]]))
        else:
            self.fileClass.setText("Unsorted")
        return

    def choice1(self):
        self.dictionary[self.fichier[self.currentIm]] = 0
        self.nextImage()

    def choice2(self):
        self.dictionary[self.fichier[self.currentIm]] = 1
        self.nextImage()

    def choice3(self):
        self.dictionary[self.fichier[self.currentIm]] = 2
        self.nextImage()

    def choice4(self):
        self.dictionary[self.fichier[self.currentIm]] = 3
        self.nextImage()

    def choice5(self):
        self.dictionary[self.fichier[self.currentIm]] = 4
        self.nextImage()
        

    def choice6(self):
        self.dictionary[self.fichier[self.currentIm]] = 5
        self.nextImage()

    def choice7(self):
        self.dictionary[self.fichier[self.currentIm]] = -1
        self.nextImage()
        

    def play(self):
        self.doPlay = not self.doPlay

    def saveDic(self):
        with io.open( self.currentDir + 'dictionnary.txt', 'wb') as outfile:
            json.dump(self.dictionary, outfile)



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
    choiceLayout = QHBoxLayout()
    nameLayout = QHBoxLayout()

    exitButton = QPushButton("Exit",window)
    playButton = QPushButton("Play",window)
    previous = QPushButton("",window)
    next = QPushButton("",window)
    saveButton = QPushButton("Save",window)

    choice1 = QPushButton("0",window)
    choice2 = QPushButton("1", window)
    choice3 = QPushButton("2",window)
    choice4 = QPushButton("3",window)
    choice5 = QPushButton("4", window)
    choice6 = QPushButton("5",window)
    choice7 = QPushButton("Pas de main",window)


    previous.setIcon(QIcon.fromTheme("go-previous"))
    next.setIcon(QIcon.fromTheme("go-next"))
    exitButton.setIcon(QIcon.fromTheme("application-exit"))
    playButton.setIcon(QIcon.fromTheme("media-playback-start"))
    saveButton.setIcon(QIcon.fromTheme("document-save"))

    nameLayout.addWidget(v.fileName)
    nameLayout.addWidget(v.fileClass)

    hLayout.addWidget(previous)
    hLayout.addWidget(v.original)
    hLayout.addWidget(v.transform1)
    hLayout.addWidget(v.transform2)
    hLayout.addWidget(v.prediction)
    hLayout.addWidget(next)

    buttonLayout.addWidget(playButton)
    buttonLayout.addWidget(saveButton)
    buttonLayout.addWidget(exitButton)

    choiceLayout.addWidget(choice1)
    choiceLayout.addWidget(choice2)
    choiceLayout.addWidget(choice3)
    choiceLayout.addWidget(choice4)
    choiceLayout.addWidget(choice5)
    choiceLayout.addWidget(choice6)
    choiceLayout.addWidget(choice7)

    vLayout.addLayout(nameLayout)
    vLayout.addLayout(hLayout)
    vLayout.addLayout(choiceLayout)
    vLayout.addLayout(buttonLayout)

    window.setLayout(vLayout)

    
    QObject.connect(previous,SIGNAL("clicked()"),v.previousImage)
    QObject.connect(next,SIGNAL("clicked()"),v.nextImage)
    QObject.connect(choice1,SIGNAL("clicked()"),v.choice1)
    QObject.connect(choice2,SIGNAL("clicked()"),v.choice2)
    QObject.connect(choice3,SIGNAL("clicked()"),v.choice3)
    QObject.connect(choice4,SIGNAL("clicked()"),v.choice4)
    QObject.connect(choice5,SIGNAL("clicked()"),v.choice5)
    QObject.connect(choice6,SIGNAL("clicked()"),v.choice6)
    QObject.connect(choice7,SIGNAL("clicked()"),v.choice7)
    QObject.connect(playButton,SIGNAL("clicked()"),v.play)
    QObject.connect(saveButton,SIGNAL("clicked()"),v.saveDic)
    QObject.connect(exitButton,SIGNAL("clicked()"),app.exit)
    
     
    window.show()
    sys.exit(app.exec_())