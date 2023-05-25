#!/bin/sh

ENABLED_PATH=~/.config/sway/device
DISABLED_PATH=~/.config/sway/disabled
CONFIG_FILE=$1

if [ -f $ENABLED_PATH/$CONFIG_FILE ]
then
	mv $ENABLED_PATH/$CONFIG_FILE $DISABLED_PATH/$CONFIG_FILE
else
	mv $DISABLED_PATH/$CONFIG_FILE $ENABLED_PATH/$CONFIG_FILE
fi

swaymsg reload
