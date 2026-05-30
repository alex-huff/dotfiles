#!/bin/sh

recordings_directory=~/minecraft/pycraft-recordings
active_recording=$(find $recordings_directory -type f -regex ".*\.pcr" -printf "%f\n" | fuzzel --dmenu)
cd $recordings_directory
ln -sf $active_recording active.pcr
