#!/bin/sh

# pip install imgur-uploader

# example configuration at ~/.config/imgur_uploader/uploader.cfg
# [imgur]
# id = ***************
# secret = ****************************************

if [ $# -ne 1 ]
then
	echo "Usage: $0 <file-path>"
	exit 1
fi
if imgur-uploader $1
then
	speak-it <<< "upload succeeded"
else
	speak-it <<< "upload failed"
fi
