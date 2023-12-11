#!/bin/sh

active_script=$(find ~/minecraft/pycraft-macros/ -type f -regex ".*\.py" -printf "%f\n" | rofi -dmenu -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
cd ~/minecraft/pycraft-macros
ln -sf $active_script active.py
