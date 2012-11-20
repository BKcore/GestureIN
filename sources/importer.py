#!/usr/bin/python

import cv
import cv2
import numpy
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="File to import", metavar="FILE")
(options, args) = parser.parse_args()

cv.NamedWindow("GestureIN", cv.CV_WINDOW_AUTOSIZE)
imagedata = cv.Load(options.filename)

def detect_hand(image, file):
    image_size = cv.GetSize(image)

    # create grayscale version
    wip = cv.CloneMat(image)
    wip8U = cv.CreateMat(wip.rows, wip.cols, cv.CV_8U)
    wipC = cv.CreateImage(image_size, 8, 3)
    #cv.ConvertScale(wip, wip, 255, 0)
    cv.ConvertImage(wip, wip8U, cv.CV_8U)
    cv.ConvertImage(wip, wipC, cv.CV_8U)

    cv.Smooth(wip8U, wip8U, cv.CV_MEDIAN)
    cv.EqualizeHist(wip8U, wip8U)
    cv.ConvertScale(wip8U, wip8U, 1, 0.92*255)
    cv.EqualizeHist(wip8U, wip8U)

    cv.ShowImage("Thresh", wip8U)
    
    # cv.NamedWindow("Original", cv.CV_WINDOW_AUTOSIZE)
    # cv.ShowImage("Original", imagedata)

    if 1 :
        # create the wanted images
        eig = cv.CreateImage(image_size, 8, 1)
        temp = cv.CreateImage(image_size, 8, 1)
        # the default parameters
        quality = 0.01
        min_distance = 6
        # search the good points
        features = cv.GoodFeaturesToTrack(wip8U, eig, temp, 40, quality, min_distance, None, 3, 0, 0.04)

        for (x,y) in features:
            cv.Circle (wipC, (int(x), int(y)), 3, (0, 255, 0), -1, 8, 0)

        hull = cv.ConvexHull2(features, cv.CreateMemStorage(), return_points=True)

        first    = None
        last     = None
        previous = None 

        for p in hull:
            if first == None:
                first = p
            else:
                cv.Line(wipC, previous, p, (0, 255, 0))                

            previous = p
            last     = p

        cv.Line(wipC, last, first, (0, 255, 0))

        contours = cv.FindContours(wip8U, cv.CreateMemStorage())
        hull     = cv.ConvexHull2(features, cv.CreateMemStorage())
        # defects  = cv.ConvexityDefects(contour, hull, cv.CreateMemStorage())

        # for p in defects:
            # print str(p)

        result = wipC

    if 0 :
        storage = cv.CreateMemStorage()
        contours = cv.FindContours(wip8U, storage, mode=cv.CV_RETR_EXTERNAL, method=cv.CV_CHAIN_APPROX_SIMPLE)

        if contours:
            while contours:
                print contours
                size = cv.ContourArea( contours );
  
                cv.DrawContours( wipC, contours, (255, 0, 0), (0, 0, 255), 1, 2 );
                contours = contours.h_next()

        result = wipC



    return result

final = detect_hand(imagedata, options.filename)

cv.ShowImage("GestureIN", final) #Show the image

cv.WaitKey(0)
cv2.destroyAllWindows()