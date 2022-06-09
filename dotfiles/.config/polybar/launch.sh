#!/usr/bin/env bash

# Terminate already running bar instances
# If all your bars have ipc enabled, you can use 
polybar-msg cmd quit
# Otherwise you can use the nuclear option:
# killall -q polybar

# Lauch bars
polybar primary 2>&1 | tee -a /tmp/polybarPrimary.log & disown
echo "Bars launched..."
