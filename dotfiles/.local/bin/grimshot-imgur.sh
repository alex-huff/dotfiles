#!/bin/bash

cd ~/screenshots
current_time=$(date +%s%9N)
image_name="screenshot-${current_time}.png"
if [ $# -gt 0 ] && [ "$1" = "area" ]
then
    slurp -y -e $image_name
    if [ $? -ne 0 ]
    then
        exit 1
    fi
else
    grim $image_name
fi
wl-copy -t image/png < $image_name
# upload-to-imgur.sh $image_name
