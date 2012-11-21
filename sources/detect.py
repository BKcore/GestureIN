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
	im = np.asarray(cv.Load(file))
	im = 255-(im/np.max(im)*255).astype('uint8')
	return im

def extractBinary(img):
	element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
	img = cv2.equalizeHist(img)
	img = cv2.erode(img, element)
	img = cv2.medianBlur(img, 3)
	#img = cv2.dilate(img, element)
	_,img = cv2.threshold(img, 0.91*255, 255, cv2.THRESH_BINARY)
	return img

img_ref = loadSample(options.filename)
img = extractBinary(img_ref)

cv2.namedWindow("Reference")
cv2.namedWindow("Debug")
cv2.imshow("Reference", img_ref)
cv2.imshow("Debug", img)

cv2.waitKey(0)
