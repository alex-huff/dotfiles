#!/bin/sh

pid=$(focused-pid.sh)
mod=$(mc-cli --pid $pid get-config-names | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
mc-cli --pid $pid open-config "$mod"
