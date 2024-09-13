#!/bin/sh

cd ~/screenshots
current_time=$(date +%s%9N)
image_name="screenshot-${current_time}.png"
if [ $1 = "area" ]
then
	temp_file=$(mktemp --suffix .png)
	grim -l 0 $temp_file
	swayimg --config='info.show=no' --fullscreen $temp_file &
	swayimg_pid=$!
	region=$(slurp -f %w:%h:%x:%y)
	slurp_return_code=$?
	kill $swayimg_pid
	if [ $slurp_return_code -ne 0 ]
	then
		rm $temp_file
		exit 1
	fi
	ffmpeg -i $temp_file -vf "crop=$region" $image_name
	rm $temp_file
else
	grim $image_name
fi
upload-to-imgur.sh $image_name
