#!/bin/zsh

rm -rf haarcascade/*

ls ./positives/*.png | python description_file_generator.py 1>positives.dat
ls ./negatives/*.png 1>negatives.dat

NB_POSITIVES=`cat positives.dat | wc -l`
NB_NEGATIVES=`cat negatives.dat | wc -l`

echo "launch createsamples"
opencv_createsamples -info positives.dat -vec positives.vec -num $NB_POSITIVES

echo "\nlaunch traincascade"
opencv_traincascade -data haarcascade -vec positives.vec -bg negatives.dat -numStages 20 -featureType LBP -numPos $NB_POSITIVES -numNeg $NB_NEGATIVES


