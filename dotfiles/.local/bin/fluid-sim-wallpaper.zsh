#!/bin/zsh

TMPSUFFIX=.html
() { kitty +kitten panel --override=window_padding_width=2 --override=font_size=0 --override=mouse_hide_wait=0 --override=background=#282828 --edge=background awrit "file://$1" } =(sed "s|{HOME}|$HOME|g" < ~/.assets/background.html)
