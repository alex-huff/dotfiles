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

# go to playlist view, got to top of current window, mute and activate selected item
cmus-remote -C "view 3" win-top "vol 0" win-activate

# identify whether we are in left or right window
# this works since:
# if we were in left window, we are now playing the only song in the top playlist, which is named $identifier
# if we were in the right window, we are now playing the top song in our current playlist, which is not named $identifier
if ! cmus-remote -Q | grep $identifier &> /dev/null
then
	# we are in right window, move to top of left
	cmus-remote -C win-next win-top
fi

# move to selected playlist, activate it, and restore volume
cmus-remote -C "win-down $(($playlist_position - 1))" win-activate "vol ${left}% ${right}%"
