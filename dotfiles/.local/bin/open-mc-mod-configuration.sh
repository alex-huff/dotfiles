#!/bin/sh

pid=$(focused-pid.sh)
mod=$(mc-cli --pid $pid get-config-names | KITTY_OVERLAY_DIMENSIONS="10:40" fzf-panel --prompt="mod: ")
mc-cli --pid $pid open-config "$mod"
