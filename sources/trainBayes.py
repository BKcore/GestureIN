#!/usr/bin/python

import cv
import cv2
import numpy as np
import os.path
from optparse import OptionParser

import detect
import dirParser
import haar

def listDirectory(path): 

    	fichier = []    
        for root, dirs, files in os.walk(path): 
            for i in files: 
                fichier.append(os.path.join(root, i)) 

        fichier.sort(key=lambda x: os.path.basename(x))
        length = len(fichier)
        return fichier


if __name__ == '__main__' :

	parser = OptionParser()
	parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
	(options, args) = parser.parse_args()


	filesNames = listDirectory(options.dirname)

	class_dict = eval(open("../bayes/dictionnary.txt").read())
	haarc = haar.haarInit(os.path.dirname(os.path.realpath(__file__)) + '/../haar/cascade.xml')

	trainData = []

	responses = []

	for fileName in filesNames:
		img_ref = detect.loadSample(fileName)
		img,rect = detect.findROI(img_ref,haarc)
		imb = detect.extractBinary(img)
		if(rect is None):
			densityVect = [-1,-1, -1, -1, -1, -1, -1, -1, -1]
		else:
			(x,y,w,h) = rect	
			if(w<5 or h<5):
				densityVect = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
			else:
				densityVect = detect.zoning(imb)	

		trainData.append(densityVect)
		responses.append(class_dict[fileName])
 	

	matrixData = np.matrix(trainData).astype('float32')
	matrixResp = np.matrix(responses)

	classifier = cv2.NormalBayesClassifier()

	classifier.train(matrixData,matrixResp)

	classifier.save('../bayes/bayes.xml')
