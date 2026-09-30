#!/bin/sh

recordings_directory=~/minecraft/pycraft-recordings
active_recording=$(find $recordings_directory -type f -regex ".*\.pcr" -printf "%f\n" | KITTY_OVERLAY_DIMENSIONS=10:40 kitty-chooser --prompt="recording: " --layout=reverse)
cd $recordings_directory
ln -sf $active_recording active.pcr
