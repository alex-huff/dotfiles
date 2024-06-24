#!/bin/sh

cd ~/screenshots
if ! [ -f recording ]
then
	current_time=$(date +%s%9N)
	grab_name="screengrab-${current_time}.mp4"
	if [ $1 = "area" ]
	then
		wf-recorder -g "$(slurp)" -f $grab_name &
	else
		wf-recorder -f $grab_name &
	fi
	printf "${grab_name}\n$!" > recording
	exit 0
fi
grab_name=$(sed -n 1p < recording)
recorder_pid=$(sed -n 2p < recording)
rm recording
kill -TERM $recorder_pid
waitpid $recorder_pid
upload-to-imgur.sh $grab_name
