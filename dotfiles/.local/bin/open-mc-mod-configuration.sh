#!/bin/sh

pid=$(focused-pid.sh)
mod=$(mc-cli --pid $pid get-config-names | fuzzel --dmenu)
mc-cli --pid $pid open-config "$mod"
