#!/bin/sh

cd ~/screenshots
current_time=$(date +%s%9N)
image_name="screenshot-${current_time}.png"
grimshot "$@" $image_name
upload-to-imgur.sh $image_name
