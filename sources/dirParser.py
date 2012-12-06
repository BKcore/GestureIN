#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser
import os.path
import Tkinter as tk


parser = OptionParser()
parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
(options, args) = parser.parse_args()

def listdirectory(path): 
    fichier=[] 
    for root, dirs, files in os.walk(path): 
        for i in files: 
            fichier.append(os.path.join(root, i)) 
    return fichier

def onKeyPress(event): 
    if(event.keysym == 'Right'):
    	print "right arrow"
    elif(event.keysym == 'Left'):
    	print "left arrow"
    else:
    	print event.keysym


files = listdirectory(options.dirname)
#print files

tkroot = tk.Tk()
tkroot.bind('<KeyPress>',  onKeyPress)             
tkroot.focus()                                     
tkroot.title('Click Me')
tkroot.mainloop()