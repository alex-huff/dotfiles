#!/bin/sh

set -e
if [ $# -lt 1 ]
then
    exit 1
fi
kitty +kitten icat --clear --transfer-mode=memory --stdin=no
file_path="$1"
mime_type="$(file -E --brief --mime-type "$1")"
case "$mime_type"
in
    text/* | application/json)
        case "$file_path"
        in
            *.md)
                mdcat --ansi "$file_path"
                ;;
            *)
                cat "$file_path"
                ;;
        esac
        ;;
    image/*)
        kitty +kitten icat --clear --transfer-mode=memory --stdin=no --place=${FZF_PREVIEW_COLUMNS}x${FZF_PREVIEW_LINES}@0x0 "$file_path"
        ;;
    *)
        file "$file_path"
        ;;
esac
