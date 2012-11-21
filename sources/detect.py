#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
parser.add_option("-m", "--mode", dest="mode", help="Detection mode (if cdt)", metavar="MODE")
(options, args) = parser.parse_args()

def loadSample(file):
    return np.asarray(cv.Load(file))

cv2.imshow("Window", loadSample(options.filename))



cv2.waitKey(0);

#detect_hand(imagedata, options.filename)
