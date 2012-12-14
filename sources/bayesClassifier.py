#!/usr/bin/python

import cv2
import numpy as np
from optparse import OptionParser


trainData = np.matrix([[0,1,1,4],[0,1,0,0],[6,2,8,1]]).astype('float32')

responses = np.matrix([0,1,2])

classifier = cv2.NormalBayesClassifier()
classifier.train(trainData,responses)

sample = np.matrix([6,2,8,0]).astype('float32')

_,result = classifier.predict(sample)

print result