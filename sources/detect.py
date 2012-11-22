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
	_, imb = cv2.threshold(img, 0.91*255, 255, cv2.THRESH_BINARY)
	return imb

def drawPolygon(im, points, color):
	first = None
	last  = None
	prev  = None

	for p in points:
		if first == None:
			first = p
		else:
			cv2.line(im, prev, p, color)

		prev = p
		last = p

	cv2.line(im, last, first, color)

def drawPoints(im, points, color, radius = 2):
	for p in points:
		cv2.circle(im, p, radius, color)

img_ref 		= loadSample(options.filename)
imb 			= extractBinary(img_ref)
imb_contours 	= imb.copy()

contours, _ = cv2.findContours(imb_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cnt32f 		= contours[0].astype('float32')
hull        = cv2.convexHull(contours[0], returnPoints=False)
# hull32f		= hull.astype('float32')
# Ici ca need du ndarray, mais je trouve pas le cv2.createMemStorage...
defects     = cv2.convexityDefects(contours[0], hull)


drawPolygon(imb_contours, [(p[0, 0], p[0, 1]) for p in contours[0]], 255)
drawPolygon(imb_contours, [(p[0, 0], p[0, 1]) for p in cv2.convexHull(contours[0])], 128)
drawPoints(imb_contours, [tuple(contours[0][p[0][2]][0]) for p in defects], 128, 3)

cv2.namedWindow("Reference")
cv2.namedWindow("Debug")
cv2.namedWindow("Contours")
cv2.imshow("Reference", img_ref)
cv2.imshow("Debug", imb)
cv2.imshow("Contours", imb_contours)

cv2.waitKey(0)
