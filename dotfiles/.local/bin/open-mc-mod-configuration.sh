#!/bin/sh

pid=$(focused-pid.sh)
mod=$(mod-menu-integration --pid $pid get-mod-names | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
mod-menu-integration --pid $pid open-config "$mod"
