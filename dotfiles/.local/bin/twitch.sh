#!/bin/sh

picked_stream=$(twitch-online-filter.py < $TWITCH_SUBS_FILE | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
streamlink "https://www.twitch.tv/$picked_stream" best
