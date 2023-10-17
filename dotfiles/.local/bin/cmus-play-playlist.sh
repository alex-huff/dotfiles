#!/bin/zsh

# get playlists, skipping first dummy playlist used for current window identification
playlists=$(ls ~/.config/cmus/playlists/ | LC_COLLATE=C sort | tail -n +2)

# get selected playlist from user
playlist=$(echo $playlists | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)

# get playlist's position in view 3
playlist_position=$(echo $playlists | grep -n "^${playlist}$" | cut -d ":" -f 1)

if [ ! $playlist_position ]
then
	echo "Invalid playlist"
	exit 1
fi

# the only song in the first dummy playlist should have this in its filename
identifier=ba304144-e8ad-42c2-9975-93e2c6d0ee56

# go to playlist view, go to top of current window, mute and activate selected item while looking for $identifier in status
cmus-remote -C "view 3" win-top mute win-activate status | grep $identifier

# return code of grep identifies whether we are in left or right window
# this works since:
# if we were in left window, we are now playing the only song in the top playlist, which is named $identifier
# if we were in the right window, we are now playing the top song in our current playlist, which is not named $identifier
if [ $pipestatus[2] -eq 1 ]
then
	# we are in right window, so we need to move to top of left first
	setup_commands=(win-next win-top)
fi

# move to selected playlist, activate it, and restore volume
cmus-remote -C $setup_commands "win-down $playlist_position" win-activate mute
