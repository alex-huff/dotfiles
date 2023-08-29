#!/bin/sh

profile=$1
subprofile=$(mm-msg profile "$profile" get-loaded-subprofiles | rofi -dmenu -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
mm-msg profile "$profile" set-subprofile "$subprofile"
