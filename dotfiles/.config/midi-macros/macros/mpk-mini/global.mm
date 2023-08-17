# subprofile switching
48{c==9} →
{
	profile="MPK mini"
	subprofile=$(mm-msg profile "$profile" get-loaded-subprofiles | rofi -dmenu -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
	mm-msg profile "$profile" set-subprofile "$subprofile"
}

# switch/move-container-to workspace
C5{v>64} *[1:]("{}"→[-]PIANO) → swaymsg move container to workspace $(echo {} | perl -pe 's/([0-9]+)/(52-$1)/eg')
C5{v<=64} *[1:]("{}"→[-]PIANO) → swaymsg workspace $(echo {} | perl -pe 's/([0-9]+)/(52-$1)/eg')

# clipboard manager
B4{v>64} *[1:]("{}"→[-]ASPN) → wl-paste -n > ~/.config/midi-macros/clipboards/"{}" && echo Saving clipboard to file: {}
B4{v<=64} *[1:]("{}"→[-]ASPN) → wl-copy < ~/.config/midi-macros/clipboards/"{}" && echo Yanking file: {} to clipboard

# main volume with knob 1
MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ pactl set-sink-volume @DEFAULT_SINK@ {}%

# cmus volume with knob 2
MIDI{STATUS==cc}{CC_FUNCTION==71}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ cmus-remote --volume {}%

# control focused application volume with knob 3
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"→f"{CC_VALUE_SCALED(0, 1)}") (python)[BLOCK|DEBOUNCE]→
{
	import subprocess
	sway_pid_extractor = subprocess.Popen(
		"swaymsg -t get_tree | jq '.. | select(.type?) | select(.focused==true).pid'",
		text=True,
		stdout=subprocess.PIPE,
		stdin=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
		shell=True
	)
	try:
		focused_pid = int(sway_pid_extractor.communicate()[0])
	except Exception:
		import sys
		sys.exit(0)
	import psutil
	focused_process = psutil.Process(focused_pid)
	process_hierarchy = {p.pid for p in focused_process.children(recursive=True)}
	process_hierarchy.add(focused_pid)
	import pulsectl
	pid_property = "application.process.id"
	with pulsectl.Pulse('mm-pulseaudio-client') as pulse:
		for sink_input in pulse.sink_input_list():
			sink_input_pid = sink_input.proplist.get(pid_property)
			if sink_input_pid and int(sink_input_pid) in process_hierarchy:
				pulse.volume_set_all_chans(sink_input, {})
				break
}

# cmus control with pads
40{c==9} → cmus-remote --pause
41{c==9} → cmus-remote --prev
42{c==9} → cmus-remote --next
43{c==9} → cmus-remote -C "toggle repeat_current"

# home assistant
(40+42){c==9} (zsh)[BLOCK|DEBOUNCE]→
{
	power_state_file=~/.config/midi-macros/state/power
	current_state=$(<$power_state_file)
	if [ $current_state = "on" ]
	then
		new_state="off"
	else
		new_state="on"
	fi
	echo $new_state > $power_state_file
	echo $(
		for i in lights lights_2 light_2 light_3 light_4; do
			hass-cli state turn_${new_state} light.color_$i &
		done
		for i in $(seq 2); do hass-cli state turn_${new_state} switch.out${i}_mss110_main_channel &; done
	)
}
(40+43){c==9} → hass-cli state toggle switch.out1_mss110_main_channel
(40+36){c==9} → hass-cli state toggle switch.out2_mss110_main_channel
# MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"→f"{CC_VALUE_SCALED(0, 1)}") [BLOCK|DEBOUNCE]→ hass-cli service call --arguments entity_id=media_player.samsung_the_frame_55,volume_level={} media_player.volume_set
MIDI{STATUS==cc}{CC_FUNCTION==74}("{}"→f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]→
{
	echo {} > ~/.config/midi-macros/state/light-r
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==75}("{}"→f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]→
{
	echo {} > ~/.config/midi-macros/state/light-g
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==76}("{}"→f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]→
{
	echo {} > ~/.config/midi-macros/state/light-b
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"→f"{round(CC_VALUE_SCALED(2000, 6500))}") [BLOCK|DEBOUNCE]→
{
	echo $(
		lights="lights lights_2 light_2 light_3 light_4"
		for light in $lights; do
			hass-cli service call --arguments "entity_id=light.color_${light},kelvin={}" light.turn_on &
		done
	)
}
MIDI{STATUS==cc}{CC_FUNCTION==77}("{}"→f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE]→
{
	echo $(
		lights="lights lights_2 light_2 light_3 light_4"
		for light in $lights; do
			hass-cli service call --arguments "entity_id=light.color_${light},brightness={}" light.turn_on &
		done
	)
}

# control panel
39{c==9} → eww open --toggle control-panel-window
MIDI{STATUS==cc}{CC_FUNCTION==74}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]→
{
	eww update light-r={}
	echo {} > ~/.config/midi-macros/state/eww-slider-r
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==75}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]→
{
	eww update light-g={}
	echo {} > ~/.config/midi-macros/state/eww-slider-g
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==76}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]→
{
	eww update light-b={}
	echo {} > ~/.config/midi-macros/state/eww-slider-b
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ eww update main-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==71}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ eww update cmus-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ eww update focused-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ eww update temperature={}
MIDI{STATUS==cc}{CC_FUNCTION==77}("{}"→CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]→ eww update brightness={}
