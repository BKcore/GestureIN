#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser
import os.path
import sys

parser = OptionParser()
parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
parser.add_option("-o", "--output", dest="output", help="Directory to output", metavar="DIRO")
parser.add_option("-x", "--xform",
                      action="store_true",
                      dest="xform_flag",
                      default=False,
                      help="bla")
(options, args) = parser.parse_args()


def listdirectory(path): 
    fichier = [] 
    
    for root, dirs, files in os.walk(path): 
        for i in files: 
            fichier.append(os.path.join(root, i)) 
    
    return fichier

files 	= listdirectory(options.dirname)
i 		= 0

for f in files:
	im = np.asarray(cv.Load(f))
	im = 255 - (im / np.max(im) * 255).astype('uint8')

	i += 1

	if (options.xform_flag == True):
		x,y = (im >= 255).nonzero()
		im[x,y] = 0


	cv2.imwrite(options.output + "/" + str(i) + ".png", im)
