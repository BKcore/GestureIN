#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser
import os.path
import Tkinter as tk
from PIL import Image, ImageTk


def listdirectory(path): 
    fichier = [] 
    
    for root, dirs, files in os.walk(path): 
        for i in files: 
            fichier.append(os.path.join(root, i)) 
    
    return fichier


def setImage(side): 
    global currentIm
    global files
    global im
    global tkroot
    global tkimage
    global window

    if(side == 1):
        currentIm = currentIm +1

    elif(side== 0):
        currentIm = currentIm -1

    im = Image.open(files[currentIm])
    tkimage = ImageTk.PhotoImage(im)
    window.config(image = tkimage)
    window.pack()


def onKeyPress(event): 
    if(event.keysym == 'Right'):
    	setImage(1)
        
    elif(event.keysym == 'Left'):
    	setImage(0)
    else:
    	print event.keysym

if __name__ == '__main__' :
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="dirname", help="Directory to parse", metavar="DIR")
    (options, args) = parser.parse_args()

    files = listdirectory(options.dirname)

    currentIm = 0
    tkroot = tk.Tk()
    im = Image.open(files[currentIm])
    tkimage = ImageTk.PhotoImage(im)
    window = tk.Label(tkroot, image=tkimage)
    window.pack()
    tkroot.bind('<KeyPress>',  onKeyPress )           
    tkroot.focus()                                     
    tkroot.title('Viewer')
    tkroot.mainloop()

