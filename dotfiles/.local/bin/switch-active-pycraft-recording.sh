#!/bin/sh

recordings_directory=~/minecraft/pycraft-recordings
active_recording=$(find $recordings_directory -type f -regex ".*\.pcr" -printf "%f\n" | rofi -dmenu -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
cd $recordings_directory
ln -sf $active_recording active.pcr
