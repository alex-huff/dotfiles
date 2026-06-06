#!/bin/sh

twitch-online-filter.py < $TWITCH_SUBS_FILE | fuzzel --dmenu --width=20 | twitch-watch-streams.py
