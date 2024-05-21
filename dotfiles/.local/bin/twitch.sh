#!/bin/sh

twitch-online-filter.py < $TWITCH_SUBS_FILE | rofi -dmenu -multi-select -i | twitch-watch-streams.py
