#!/usr/bin/python

import cv
import cv2
import numpy as np
from optparse import OptionParser
import os.path
import Tkinter as tk
from PIL import Image, ImageTk
import detect

def listdirectory(path): 
    fichier = [] 
    
    for root, dirs, files in os.walk(path): 
        for i in files: 
            fichier.append(os.path.join(root, i)) 
    
    return fichier


def setImage(side): 
    global currentIm
    global length
    global files
    global window

    if(side == 1):
        currentIm = currentIm +1
        if (currentIm > length-1):
            currentIm = 0

    elif(side== 0):
        currentIm = currentIm -1
        if (currentIm < 0):
            currentIm = length-1

    displayImage(currentIm,files, window)

def displayImage(index,files,window):
   
    im = Image.open(files[index])
    tkimage = ImageTk.PhotoImage(im)  
    window.configure(image = tkimage)
    window.pack()
    return
    
    img2,img3 = detect.loadAndProcess(files[index])

    im2 = Image.fromarray(img2)
    tkimage2 = ImageTk.PhotoImage(im2)
    window2.configure(image = tkimage2)
    window2.pack()

    im3 = Image.fromarray(img3)
    tkimage3 = ImageTk.PhotoImage(im3)
    window3.configure(image = tkimage3)
    window3.pack()


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
    length = len(files)

    

    currentIm = 0
    tkroot = tk.Tk()
    im = Image.open(files[0])
    tkimage = ImageTk.PhotoImage(im)  

    window = tk.Label(tkroot, image = tkimage)
    window.pack()
    #window2 = tk.Label(tkroot)
    #window3 = tk.Label(tkroot)
    #displayImage(currentIm,files,window)
    tkroot.bind('<KeyPress>',  onKeyPress )           
    tkroot.focus()                                     
    tkroot.title('Viewer')
    tkroot.mainloop()