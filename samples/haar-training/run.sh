#!/bin/zsh

find positives -name '*.png' -exec identify -format 'positives/%f 1 0 0 %w %h' '{}' \; 1>positives.dat
find negatives -name '*.png' 1>negatives.dat

NB_POSITIVES=`cat positives.dat | wc -l`
NB_NEGATIVES=`cat negatives.dat | wc -l`

echo "launch createsamples"
opencv_createsamples -info positives.dat -vec positives.vec -w 48 -h 48 -num $NB_POSITIVES

echo "\nlaunch traincascade"
opencv_traincascade -data haarcascade -vec positives.vec -bg negatives.dat -numStages 20 -w 48 -h 48 -numPos $NB_POSITIVES -numNeg $NB_NEGATIVES