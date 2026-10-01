#!/bin/sh

profile=$1
subprofile=$(mm-msg profile "$profile" get-loaded-subprofiles | KITTY_OVERLAY_DIMENSIONS=10:40 fzf-panel --prompt="subprofile: ")
mm-msg profile "$profile" set-subprofile "$subprofile"
