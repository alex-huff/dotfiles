#!/bin/sh

swaymsg -t get_tree | jq "recurse(.floating_nodes[], .nodes[]) | select(.focused==true).pid"
