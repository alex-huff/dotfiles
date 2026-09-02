#!/bin/sh

twitch-online-filter.py < $TWITCH_SUBS_FILE | kitty-chooser | twitch-watch-streams.py
