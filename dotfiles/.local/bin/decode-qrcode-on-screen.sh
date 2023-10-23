#!/bin/sh

image_path=~/screenshots/current-screen.png
grimshot save active $image_path &> /dev/null
decode-qrcode.py $image_path
