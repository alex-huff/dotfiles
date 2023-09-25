#!/bin/sh

default_sink=$(pactl get-default-sink)
pactl load-module module-null-sink sink_name=hear
pactl load-module module-null-sink sink_name=hush
hear_sink=$(pactl list sinks short | grep hear | cut -f 1)
hush_sink=$(pactl list sinks short | grep hush | cut -f 1)
pactl load-module module-loopback source=$hear_sink sink=$default_sink
pactl load-module module-loopback source=$hush_sink sink=$default_sink
pactl set-default-sink $hear_sink
