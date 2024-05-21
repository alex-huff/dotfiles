#!/bin/sh

pid=$(focused-pid.sh)
mod=$(mc-cli --pid $pid get-config-names | rofi -dmenu -i)
mc-cli --pid $pid open-config "$mod"
