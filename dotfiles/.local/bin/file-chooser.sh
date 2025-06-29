#!/bin/sh

CHOICE=$5 RECOMMENDED_SAVE_PATH=$4 CHOOSER='xargs -d "\n" realpath >> "$CHOICE"' kitty --app-id=kitty-dialogue bash --login
