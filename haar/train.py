 #!/usr/bin/env python

import os
import sys

nb_positives = 0
nb_negatives = 0
min_hit_rate = 0.995

with open('positives.dat', 'r') as f:
	for l in f.readlines():
		nb_positives += 1

with open('negatives.dat', 'r') as f:
	for l in f.readlines():
		nb_negatives += 1

nb_positives_traincascade = int(nb_positives * min_hit_rate * 0.9)

os.system("""opencv_traincascade	-data training -vec positives.vec -bg negatives.dat \\
									-w 48 -h 48 \\
									-precalcValBufSize 1024 -precalcIdxBufSize 2047 \\
									-numStages 20 \\
									-minHitRate {0} \\
									-numPos {1} -numNeg {2}""".format(min_hit_rate, nb_positives_traincascade, nb_negatives))