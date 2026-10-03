#!/bin/sh

if [ $# -lt 3 ]
then
    exit 1
fi

extract_basename_python_script=$(
	cat <<-EOF
		import sys
		from urllib.parse import urlparse, unquote

		url = sys.argv[1]
		parsed_url = urlparse(url)
		unquoted_path = unquote(parsed_url.path)
		assert len(unquoted_path)
		basename = unquoted_path[unquoted_path.rindex("/") + 1:]
		assert "\0" not in basename

		print(basename, end="")
	EOF
)

preview_image_url="$4"
preview_image_url_basename=$(python3 -c "$extract_basename_python_script" "$preview_image_url" 2> /dev/null)
if [ -z "$preview_image_url_basename" ]
then
	exit 1
fi

cached_image_path="${FZF_PANEL_TEMPDIR}/${preview_image_url_basename}"

if [ ! -f "$cached_image_path" ]
then
    curl --location --ipv4 --output "$cached_image_path" "$preview_image_url" &> /dev/null
fi

printf "%s\n%s\n⏺ %s Viewers\n" "$1" "$2" "$3"
kitty +kitten icat --clear --transfer-mode=memory --stdin=no --place=${FZF_PREVIEW_COLUMNS}x$((${FZF_PREVIEW_LINES}-3))@0x0 "$cached_image_path"
