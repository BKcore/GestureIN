#!/usr/bin/env python

import cv2
import numpy
import sys

for line in sys.stdin:
	line = line.rstrip("\n\r")
	size = cv2.imread("./" + line).shape
	print line + "\t1\t0 0 " + str(size[0]) + " " + str(size[1])
