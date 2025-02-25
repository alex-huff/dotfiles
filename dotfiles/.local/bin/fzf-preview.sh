#!/bin/sh

set -e
if [ $# -lt 2 ]
then
    exit 1
fi
bat_command=$(command -v bat || command -v batcat || echo :)
icat_transfer_mode=$1
file_path=$2
mime_type=$(file -E --dereference --brief --mime-type "$file_path")
kitty +kitten icat --clear --transfer-mode=$icat_transfer_mode --stdin=no
case "$mime_type"
in
    text/* | application/json)
        $bat_command --color=always --style=plain "$file_path"
        ;;
    image/*)
        kitty +kitten icat --clear --transfer-mode=$icat_transfer_mode --stdin=no --place=${FZF_PREVIEW_COLUMNS}x${FZF_PREVIEW_LINES}@0x0 "$file_path"
        ;;
    *)
        file "$file_path" | fold --width=$FZF_PREVIEW_COLUMNS
        ;;
esac
