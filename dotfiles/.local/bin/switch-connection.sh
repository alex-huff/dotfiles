#!/bin/sh

nmcli connection up $(nmcli --get-values name connection show | KITTY_OVERLAY_DIMENSIONS="10:40" kitty-chooser --prompt="connection: " --layout=reverse)
