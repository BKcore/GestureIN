#!/usr/bin/python

import cv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
(options, args) = parser.parse_args()

cv.NamedWindow("GestureIN", cv.CV_WINDOW_AUTOSIZE)
imagedata = cv.Load(options.filename)
cv.ShowImage("GestureIN", imagedata) #Show the image
cv.WaitKey(0)