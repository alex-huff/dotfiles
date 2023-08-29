#!/bin/sh

swaymsg -t get_tree | jq ".. | select(.type?) | select(.focused==true).pid"
