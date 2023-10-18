#!/bin/sh

twitch-online-filter.py < $TWITCH_SUBS_FILE | rofi -dmenu -multi-select -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi | twitch-watch-streams.py
