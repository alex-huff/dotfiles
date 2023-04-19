#!/bin/sh

# pip install imgur-uploader

# example configuration at ~/.config/imgur_uploader/uploader.cfg
# [imgur]
# id = ***************
# secret = ****************************************

cd ~/screenshots
current_time=$(date +%s%9N)
image_name="screenshot-${current_time}.png"
grimshot "$@" $image_name
imgur-uploader $image_name
