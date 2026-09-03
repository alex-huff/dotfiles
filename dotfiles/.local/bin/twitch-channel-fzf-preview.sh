#!/bin/sh

if [ $# -lt 3 ]
then
    exit 1
fi

printf "%s\n⏺ %s Viewers\n" "$1" "$2"
kitty +kitten icat --clear --transfer-mode=memory --stdin=no --place=${FZF_PREVIEW_COLUMNS}x${FZF_PREVIEW_LINES}@0x0 "$3"
