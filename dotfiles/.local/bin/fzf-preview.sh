#!/bin/sh

set -e
if [ $# -lt 1 ]
then
    exit 1
fi
if [ -n "${SSH_CLIENT+_}" ]
then
    icat_transfer_mode=memory
else
    icat_transfer_mode=stream
fi
bat_command=$(command -v bat || command -v batcat || echo :)
file_path="$1"
mime_type="$(file -E --dereference --brief --mime-type "$1")"
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
