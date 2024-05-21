#!/bin/sh

profile=$1
subprofile=$(mm-msg profile "$profile" get-loaded-subprofiles | rofi -dmenu)
mm-msg profile "$profile" set-subprofile "$subprofile"
