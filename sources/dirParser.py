#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser
import os.path

parser = OptionParser()
parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
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

	cv2.imwrite(options.dirname + "/img/" + str(i) + ".png", im)
