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
	img = cv2.dilate(img, element)
	_, imb = cv2.threshold(img, 0.92*255, 255, cv2.THRESH_BINARY)
	return imb

def drawPolygon(im, points, color, thickness=1):

	first = None
	last  = None
	prev  = None

	for p in points:
		if first == None:
			first = p
		else:
			cv2.line(im, prev, p, color, thickness)

		prev = p
		last = p

	cv2.line(im, last, first, color, thickness)

def drawPoints(im, points, color, radius = 2):
	for p in points:
		cv2.circle(im, p, radius, color, -1)

def bestContourAsInt(contours, minArea = -1):
	maxArea = -1
	contour = None

	for cnt in contours:
		cnt_int = cnt.astype('int')
		area = cv2.contourArea(cnt_int)
		if(area > maxArea and area > minArea):
			contour = cnt_int
			maxArea = area

	return contour

def refineHullDefects(hull, defects, contour, thresh):
	hull_refined = list(hull)
	defects_points = list()

	for d in defects:
		index = hull.index(tuple(contour[d[0][0]][0]))
		value = tuple(contour[d[0][2]][0])
		print d[0][3]
		if(d[0][3] > thresh):
			hull_refined.insert(index, value)
			defects_points.append(value)

	return hull_refined, defects_points

def drawResult(im, hull, defects, shape):
	imc = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)

	drawPolygon(imc, hull, (0, 255, 255), 2)
	drawPolygon(imc, shape, (0, 255, 0), 2)
	drawPoints(imc, defects, (255, 0, 0), 4)

	return imc
	

img_ref				= loadSample(options.filename)
imb						= extractBinary(img_ref)
imb_contours 	= imb.copy()

contours, _ = cv2.findContours(imb_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour 		= bestContourAsInt(contours)
hull        = cv2.convexHull(contour, returnPoints=False).astype('int')
defects     = cv2.convexityDefects(contour, hull)

hull_points 		= [tuple(p[0]) for p in cv2.convexHull(contour, returnPoints=True)]
contour_points 	= [tuple(p[0]) for p in contour]

hull_refined, defects_points = refineHullDefects(hull_points, defects, contour, 2500)

# Debug
drawPolygon(imb_contours, contour_points, 255)
drawPolygon(imb_contours, hull_refined, 128, 2)
drawPoints(imb_contours, defects_points, 128, 3)

img_result = drawResult(img_ref, hull_points, defects_points, hull_refined)

cv2.namedWindow("Debug")
cv2.namedWindow("Result")
cv2.imshow("Debug", imb_contours)
cv2.imshow("Result", img_result)

cv2.waitKey(0)
