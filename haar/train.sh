#!/bin/zsh

find positives -name '*.png' -exec identify -format '../positives/%f 1 0 0 %w %h' '{}' \; 1>training/positives.dat
find negatives -name '*.png' -exec echo '../{}' \; 1>training/negatives.dat

NB_POSITIVES=`cat training/positives.dat | wc -l`
NB_NEGATIVES=`cat training/negatives.dat | wc -l`

echo "launch createsamples"
opencv_createsamples -info training/positives.dat -vec training/positives.vec -w 48 -h 48 -num $NB_POSITIVES

echo "\nlaunch traincascade"
opencv_traincascade -data training -vec training/positives.vec -bg training/negatives.dat -numStages 20 -w 48 -h 48 -precalcValBufSize 1024 -precalcIdxBufSize 1024 -minHitRate 0.95 -numPos $NB_POSITIVES -numNeg $NB_NEGATIVES