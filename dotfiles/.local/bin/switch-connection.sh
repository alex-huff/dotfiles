#!/bin/sh

nmcli connection up $(nmcli --get-values name connection show | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
