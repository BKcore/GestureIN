#!/usr/bin/python

import cv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
(options, args) = parser.parse_args()

cv.NamedWindow("GestureIN", cv.CV_WINDOW_AUTOSIZE)
imagedata = cv.Load(options.filename)

def detect_hand(image):
    image_size = cv.GetSize(image)

    # create grayscale version
    wip = cv.CloneMat(image)
    wip8U = cv.CreateMat(wip.rows, wip.cols, cv.CV_8U)
    #cv.ConvertScale(wip, wip, 255, 0)
    cv.ConvertImage(wip, wip8U, cv.CV_8U)

    cv.Smooth(wip8U, wip8U, cv.CV_MEDIAN)
    cv.EqualizeHist(wip8U, wip8U)

    return wip8U

final = detect_hand(imagedata)

cv.NamedWindow("Original", cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage("Original", imagedata)

cv.ShowImage("GestureIN", final) #Show the image

cv.WaitKey(0)