#!/bin/sh

if [ $# -ne 1 ]
then
	echo "Usage: $0 <playlist>"
	exit 1
fi

playlist=$1
playlist_position=$(ls ~/.config/cmus/playlists | LC_COLLATE=C sort | grep -n "^${1}$" | cut -d ":" -f 1)

if [ ! $playlist_position ]
then
	echo "Invalid playlist"
	exit 1
fi

identifier=ba304144-e8ad-42c2-9975-93e2c6d0ee56

# save vol_left and vol_right
read -d "\n" left right < <(cmus-remote -Q | grep --extended-regexp "vol_(left|right)" | cut -d " " -f 3)

# go to playlist view
cmus-remote -C "view 3"

# go to top of window
cmus-remote -C win-top

# mute
cmus-remote -C "vol 0"

# activate either 000 playlist or top song in current playlist
cmus-remote -C win-activate

# identify whether we are in left or right window
if ! cmus-remote -Q | grep $identifier &> /dev/null
then
	# if in right window, move to top of left
	cmus-remote -C win-next
	cmus-remote -C win-top
fi

# move to selected playlist
cmus-remote -C "win-down $(($playlist_position - 1))"

# play playlist
cmus-remote -C win-activate

# restore volume
cmus-remote -C "vol ${left}% ${right}%"
