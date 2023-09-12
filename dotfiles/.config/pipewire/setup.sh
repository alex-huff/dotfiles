#!/bin/sh

default_sink=$(pactl get-default-sink)
pactl load-module module-null-sink sink_name=hear
pactl load-module module-null-sink sink_name=hush
pactl load-module module-loopback source=hear sink=$default_sink
pactl load-module module-loopback source=hush sink=$default_sink
pactl set-default-sink hear
