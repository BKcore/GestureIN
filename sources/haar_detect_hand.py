#!/usr/bin/env python

import cv2
from optparse import OptionParser

def detect_hands(im, cascade_xml):
	return cv2.CascadeClassifier(cascade_xml).detectMultiScale(im)

if __name__ == '__main__' :
	parser = OptionParser()
	parser.add_option("-c", "--cascade-xml", dest="cascade_xml", help="Haar cascade xml file", metavar="DIR")
	parser.add_option("-i", "--image", dest="image", help="Image to work on")
	(options, args) = parser.parse_args()

	im = cv2.imread(options.image)
	hands = detect_hands(im, options.cascade_xml)

	for (x,y,w,h) in hands:
		cv2.rectangle(im, (x,y), (x+w,y+h), 255)

	cv2.namedWindow("Hand Detection")
	cv2.imshow("Hand Detection", im)

	cv2.waitKey(0)



