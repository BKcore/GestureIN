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
    fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            fichier.append(os.path.join(root, i)) 
    return fichier


files = listdirectory(options.dirname)
print files

