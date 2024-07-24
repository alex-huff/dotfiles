#!/bin/bash

state_dir=~/.config/midi-macros/state/
r=$(<${state_dir}light-r)
g=$(<${state_dir}light-g)
b=$(<${state_dir}light-b)
echo $(
	for light in $(seq 5)
	do
		hass-cli raw ws --json "{\"domain\":\"light\",\"service\":\"turn_on\",\"service_data\":{\"entity_id\":\"light.clc${light}\",\"rgb_color\":[$r,$g,$b]}}" call_service &
	done
)
