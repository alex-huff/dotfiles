#!/bin/bash

state_dir=~/.config/midi-macros/state/
r=$(<${state_dir}light-r)
g=$(<${state_dir}light-g)
b=$(<${state_dir}light-b)
lights="lights lights_2 light_2 light_3 light_4"
echo $(
	for light in $lights
	do
		hass-cli raw ws --json "{\"domain\":\"light\",\"service\":\"turn_on\",\"service_data\":{\"entity_id\":\"light.color_${light}\",\"rgb_color\":[$r,$g,$b]}}" call_service &
	done
)
