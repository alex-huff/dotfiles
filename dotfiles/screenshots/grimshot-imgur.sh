#!/bin/sh

cd ~/screenshots
current_time=$(date +%s%9N)
image_name="screenshot-${current_time}.png"
if [ $1 = "area" ]
then
	temp_file=$(mktemp --suffix .png)
	grim -l 0 $temp_file
	swayimg --config='Textinfo.show=no' --fullscreen $temp_file &
	swayimg_pid=$!
	region=$(slurp -f %w:%h:%x:%y)
	if [ $? -ne 0 ]
	then
		region='in_w:in_h:0:0'
	fi
	kill $swayimg_pid
	ffmpeg -i $temp_file -vf "crop=$region" $image_name
else
	grim $image_name
fi
upload-to-imgur.sh $image_name
