#!/bin/sh
FOCUSED_ID=$(swaymsg -t get_tree | jq '.. | select(.type?) | select(.focused==true).pid')
kill -9 $FOCUSED_ID
