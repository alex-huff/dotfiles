#!/bin/zsh

TMPSUFFIX=.html
() { kitty +kitten panel --override=font_size=0 --override=window_padding_width=0 --override=mouse_hide_wait=0 --edge=background awrit "file://$1" } =(sed "s|{HOME}|$HOME|g" < ~/.assets/background.html)
