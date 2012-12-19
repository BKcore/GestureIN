 #!/usr/bin/env python

import os
import sys
import cv2
import numpy

nb_positives = 0
nb_negatives = 0
min_hit_rate = 0.995

with open('training/positives.dat', 'w') as out:
	for root, dirs, files in os.walk('positives/'):
		for f in files:
			nb_positives += 1
			im_shape = cv2.imread('positives/' + str(f)).shape
			out.write('../positives/{:s} 1 0 0 {:d} {:d}\n'.format(f, im_shape[0], im_shape[1]))

with open('training/negatives.dat', 'w') as out:
	for root, dirs, files in os.walk('negatives/'):
		for f in files:
			nb_negatives += 1
			out.write('../negatives/{:s}\n'.format(f))

nb_positives_traincascade = round(nb_positives * min_hit_rate * 0.9)

print "launch createsamples"
os.system(
	"""opencv_createsamples	-info training/positives.dat -vec training/positives.vec \
							-w 48 -h 48 \
							-num {0} \
							# -show""".format(nb_positives))

print "\nlaunch traincascade"
os.system(
	"""opencv_traincascade	-data training -vec training/positives.vec -bg training/negatives.dat \
							-w 48 -h 48 \
							-precalcValBufSize 1024 -precalcIdxBufSize 1024 \
							-numStages 20 \
							-minHitRate {0} \
							-numPos {1} -numNeg {2}""".format(min_hit_rate, nb_positives_traincascade, nb_negatives))