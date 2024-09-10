#!/bin/sh

cd ~/screenshots
if ! [ -f recording ]
then
	current_time=$(date +%s%9N)
	grab_name="screengrab-${current_time}.mp4"
	if [ $1 = "area" ]
	then
		area="$(slurp)"
		wf-recorder --framerate 30 -g "$area" -f $grab_name &
	else
		wf-recorder --framerate 30 -f $grab_name &
	fi
	speak-it <<< "recording"
	printf "${grab_name}\n$!" > recording
	exit 0
fi
grab_name=$(sed -n 1p < recording)
recorder_pid=$(sed -n 2p < recording)
rm recording
kill -TERM $recorder_pid
waitpid $recorder_pid
speak-it <<< "recording saved"
# upload-to-imgur.sh $grab_name
