#!/bin/sh

playlist=$(ls ~/.config/cmus/playlists | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
playlist_position=$(ls ~/.config/cmus/playlists | LC_COLLATE=C sort | grep -n "^${playlist}$" | cut -d ":" -f 1)

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
	# we are in right window, move to top of left
	cmus-remote -C win-next
	cmus-remote -C win-top
fi

# move to selected playlist
cmus-remote -C "win-down $(($playlist_position - 1))"

# play playlist
cmus-remote -C win-activate

# restore volume
cmus-remote -C "vol ${left}% ${right}%"
