#!/bin/sh

nmcli connection up $(nmcli --get-values name connection show | fuzzel --dmenu)
