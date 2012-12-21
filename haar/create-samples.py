 #!/usr/bin/env python

import os
import sys
import cv2
import numpy

nb_positives = 0
nb_negatives = 0
min_hit_rate = 0.995

with open('positives.dat', 'w') as out:
	for root, dirs, files in os.walk('positives/'):
		for f in files:
			nb_positives += 1
			im_shape = cv2.imread('positives/' + str(f)).shape
			out.write('positives/{:s} 1 0 0 {:d} {:d}\n'.format(f, im_shape[0], im_shape[1]))

with open('negatives.dat', 'w') as out:
	for root, dirs, files in os.walk('negatives/'):
		for f in files:
			nb_negatives += 1
			out.write('negatives/{:s}\n'.format(f))

nb_positives_traincascade = int(nb_positives * min_hit_rate * 0.9)

os.system("""opencv_createsamples	-info positives.dat -vec positives.vec \\
									-w 48 -h 48 \\
									-num {0} \\
									# -show""".format(nb_positives))