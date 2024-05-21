#!/bin/sh

nmcli connection up $(nmcli --get-values name connection show | rofi -dmenu -i)
