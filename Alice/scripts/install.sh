#!/bin/bash
cd .data
rm -r darknet
git clone https://github.com/pjreddie/darknet.git
cd darknet
make
curl -O https://pjreddie.com/media/files/darknet19.weights
curl -O https://pjreddie.com/media/files/yolov3-tiny.weights
