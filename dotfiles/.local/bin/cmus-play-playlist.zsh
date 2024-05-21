#!/bin/zsh

# get playlists, skipping first dummy playlist used for current window identification
playlists=$(ls ~/.config/cmus/playlists/ | LC_COLLATE=C sort | tail -n +2)

# get selected playlist from user
playlist=$(echo $playlists | rofi -dmenu -i)

# get playlist's position in view 3
playlist_position=$(echo $playlists | grep -n "^${playlist}$" | cut -d ":" -f 1)

if [ ! $playlist_position ]
then
	echo "Invalid playlist"
	exit 1
fi

# the only song in the first dummy playlist should have this in its filename
identifier=ba304144-e8ad-42c2-9975-93e2c6d0ee56

# go to playlist view, go to top of current window, and activate selected item while looking for $identifier in filename
cmus-remote -C "view 3" win-top win-activate "format_print %F" | grep $identifier

# return code of grep identifies whether we are in the playlist or track window
# this works since:
# if we were in the playlist window, we are now playing the only song in the top playlist, which has $identifier in filename
# if we were in the track window, we are now playing the top song in our current playlist, which does not have $identifier in filename
if [ $pipestatus[2] -eq 1 ]
then
	# we are in track window, so we need to move to top of playlist window
	setup_commands=(win-next win-top)
fi

# move to selected playlist, and activate it
cmus-remote -C $setup_commands "win-down $playlist_position" win-activate
