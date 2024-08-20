# subprofile switching
48{c==9} -> switch-mm-subprofile.sh "MPK mini"

# switch/move-container-to workspace
C5{v>64} NOTES[1:]("{}"->[-]f"{72 - MIDI}") -> swaymsg move container to workspace {}
C5{v<=64} NOTES[1:]("{}"->[-]f"{72 - MIDI}") -> swaymsg workspace {}

# clipboard manager
B4{v>64} NOTES[1:]("{}"->[-]ASPN) -> wl-paste -n > ~/.config/midi-macros/clipboards/{} && echo Saving clipboard to file: {}
B4{v<=64} NOTES[1:]("{}"->[-]ASPN) -> wl-copy < ~/.config/midi-macros/clipboards/{} && echo Yanking file: {} to clipboard

# lock/unlock
(43+39){c==9} -> $(which kill) -USR1 swaylock || swaylock -c 000000 --font "Victor Mono"
(39+43){c==9} -> swaymsg output '$main_display' toggle

# main volume with knob 1
MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> pactl set-sink-volume $MAIN_SINK {}%

# cmus volume with knob 2
MIDI{STATUS==cc}{CC_FUNCTION==71}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> cmus-remote --volume {}%

# control focused application volume with knob 3
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->f"{CC_VALUE_SCALED(0, 1)}") (python)[BLOCK|DEBOUNCE]->
{
	import subprocess
	focused_pid = int(
		subprocess.check_output(
			"focused-pid.sh",
			text=True,
			shell=True
		)
	)
	import psutil
	focused_process = psutil.Process(focused_pid)
	process_hierarchy = {p.pid for p in focused_process.children(recursive=True)}
	process_hierarchy.add(focused_pid)
	import pulsectl
	pid_property = "application.process.id"
	with pulsectl.Pulse("mm-pulseaudio-client") as pulse:
		for sink_input in pulse.sink_input_list():
			sink_input_pid = sink_input.proplist.get(pid_property)
			if sink_input_pid and int(sink_input_pid) in process_hierarchy:
				pulse.volume_set_all_chans(sink_input, {})
				break
}

# laptop brightness
E3 MIDI{STATUS==cc}{CC_FUNCTION==72}(CC_VALUE_PERCENT) [BACKGROUND|INVOCATION_FORMAT=f"{a}\n"|KILL]->
{
	while true
	do
		ssh alex@archl zsh -c '"xargs -I {} echo {} > /sys/class/backlight/amdgpu_bl1/brightness"'
		sleep 30
	done
}

# cmus
40{c==9} -> cmus-remote --pause
41{c==9} -> cmus-remote --prev
42{c==9} -> cmus-remote --next
43{c==9} -> cmus-remote -C "toggle repeat_current"
C3 MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->CC_VALUE) [BLOCK|DEBOUNCE]->
{
	current_song_duration=$(cmus-remote -Q | grep duration | cut -d " " -f 2)
	cmus-remote --seek $(python -c "print(round(({} / 127) * $current_song_duration))")
}

# mpv
MIDI{STATUS==pb}("{}"->f"{DATA_2_SCALED(-57/7, 10):.2f}") (python)[BLOCK|DEBOUNCE]->
{
	import subprocess
	import json
	playback_rate = {}
	focused_pid = int(subprocess.check_output('focused-pid.sh'))
	speed_command = {'command': ['set_property', 'speed', abs(playback_rate)]}
	direction_command = {'command': ['set_property', 'play-direction', 'forward' if playback_rate > 0 else 'backward']}
	display_command = {'command': ['show-text', f'Playback Rate: {playback_rate}']}
	json_payload = '\n'.join(json.dumps(command) for command in (speed_command, direction_command, display_command))
	subprocess.run(f"echo '{json_payload}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-{focused_pid}.sock", shell=True)
}
36{c==9} -> echo '{"command": ["cycle", "pause"]}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock
37{c==9} -> echo '{"command": ["playlist-prev"]}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock
38{c==9} -> echo '{"command": ["playlist-next"]}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock
39{c==9} ->
{
	sock_path=$XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock
	loop_state=$(printf '{"command": ["cycle-values", "loop-file", "inf", "no"]}\n{"command": ["get_property", "loop-file"]}\n' | socat - $sock_path | jq -sr '.[1].data')
	echo '{"command": ["show-text", "Loop: '$loop_state'"]}' | socat - $sock_path
}
(36+37){c==9} -> echo '{"command": ["revert-seek"]}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->f"{round(CC_VALUE_SCALED(0, 130))}") [BLOCK|DEBOUNCE]->
{
	socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock <<EOF
	{"command": ["set_property", "volume", {}]}
	{"command": ["show-text", "Volume: {}%"]}
	EOF
}

# clipper
C4 NOTES[0:1](ASPN) (python $MM_SCRIPT)[BACKGROUND|INVOCATION_FORMAT=f"{a}\n"]->
{
	import os
	import sys
	import subprocess
	import time
	import threading
	import shutil
	import json
	import obswebsocket

	def speak(to_speak):
		speech_process = subprocess.Popen('speak-it', stdin=subprocess.PIPE, text=True)
		speech_process.stdin.write(to_speak)
		speech_process.stdin.close()

	def save_obs_replay():
		global websocket_save_finished
		with websocket_save_finished_condition:
			websocket_save_finished = False
			succeeded = websocket.call(obswebsocket.requests.SaveReplayBuffer()).status
			if not succeeded:
				return False
			return websocket_save_finished_condition.wait_for(lambda: websocket_save_finished, timeout=20)

	def get_current_timestamp_in_mpv():
		json_result = subprocess.check_output('echo \'{"command": ["get_property", "playback-time"]}\' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock', shell=True, text=True)
		if not json_result:
			return False, -1
		json_result_object = json.loads(json_result)
		if json_result_object['error'] != 'success':
			return False, -1
		return True, json_result_object["data"]

	def open_video_in_mpv(video_path):
		return subprocess.Popen((mpv_path, '--wayland-app-id=mpv-clipper', video_path))

	def clip_video(video_path, beginning_timestamp, end_timestamp):
		duration = end_timestamp - beginning_timestamp
		if duration < 0:
			return False, ''
		out_path = f'{video_path}-clipped.mp4'
		clipper_process = subprocess.run(f'ffmpeg -ss {beginning_timestamp} -i "{video_path}" -t {duration} "{out_path}"', shell=True)
		return clipper_process.returncode == 0, out_path

	def on_replay_saved(event):
		global replay_video_path, websocket_save_finished
		with websocket_save_finished_condition:
			replay_video_path = event.datain['savedReplayPath']
			websocket_save_finished = True
			websocket_save_finished_condition.notify_all()

	websocket_host = 'localhost'
	websocket_port = 4455
	websocket_password = os.environ['OBS_WEBSOCKET_PASSWORD']
	websocket = obswebsocket.obsws(websocket_host, websocket_port, websocket_password)
	websocket.register(on_replay_saved, obswebsocket.events.ReplayBufferSaved)
	websocket.connect()
	mpv_path = shutil.which('mpv')
	currently_clipping = False
	beginning_timestamp = end_timestamp = replay_video_path = clipping_mpv_process = None
	websocket_save_finished = False
	websocket_save_finished_condition = threading.Condition()
	for line in sys.stdin:
		line = line.rstrip()
		match line:
			case '':
				if currently_clipping:
					clipping_mpv_process.kill()
					clipping_mpv_process.wait()
					if None in (beginning_timestamp, end_timestamp):
						speak('cancelling')
					else:
						speak('saving')
						succeeded, clip_video_path = clip_video(replay_video_path, beginning_timestamp, end_timestamp)
						speak(f'clipping {"succeeded" if succeeded else "failed"}')
						if succeeded:
							open_video_in_mpv(clip_video_path)
					beginning_timestamp = end_timestamp = None
				else:
					succeeded = save_obs_replay()
					if not succeeded:
						speak('failed to save replay')
						continue
					clipping_mpv_process = open_video_in_mpv(replay_video_path)
				currently_clipping = not currently_clipping
			case 'B3' | 'D4':
				if not currently_clipping:
					continue
				currently_setting_beginning_timestamp = line == 'B3'
				succeeded, timestamp = get_current_timestamp_in_mpv()
				if succeeded:
					if currently_setting_beginning_timestamp:
						beginning_timestamp = timestamp
					else:
						end_timestamp = timestamp
					speak(f'set clip {"beginning" if currently_setting_beginning_timestamp else "end"}')
				else:
					speak('could not retrieve timestamp')
			case _:
				pass
}

# home assistant
(40+41){c==9} (zsh)[BLOCK|DEBOUNCE]->
{
	power_state_file=~/.config/midi-macros/state/power
	current_state=$(<$power_state_file)
	if [ $current_state = on ]
	then
		new_state=off
	else
		new_state=on
	fi
	echo $new_state > $power_state_file
	echo $(
		for light in $(seq 5)
		do
			hass-cli state turn_${new_state} light.clc${light} &
		done
		for switch in $(seq 2)
		do
			hass-cli state turn_${new_state} switch.out${switch}_mss110_main_channel &
		done
	)
}
(40+42){c==9} -> hass-cli state toggle switch.out1_mss110_main_channel
(40+43){c==9} -> hass-cli state toggle switch.out2_mss110_main_channel
# MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"->f"{CC_VALUE_SCALED(0, 1)}") [BLOCK|DEBOUNCE]-> hass-cli service call --arguments entity_id=media_player.samsung_the_frame_55,volume_level={} media_player.volume_set
MIDI{STATUS==cc}{CC_FUNCTION==74}("{}"->f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]->
{
	echo {} > ~/.config/midi-macros/state/light-r
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==75}("{}"->f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]->
{
	echo {} > ~/.config/midi-macros/state/light-g
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==76}("{}"->f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE|LOCK=light]->
{
	echo {} > ~/.config/midi-macros/state/light-b
	~/.config/midi-macros/scripts/update-lights.bash
}
MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"->f"{round(CC_VALUE_SCALED(2000, 6500))}") [BLOCK|DEBOUNCE]->
{
	echo $(
		for light in $(seq 5)
		do
			hass-cli service call --arguments "entity_id=light.clc${light},kelvin={}" light.turn_on &
		done
	)
}
MIDI{STATUS==cc}{CC_FUNCTION==77}("{}"->f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE]->
{
	echo $(
		for light in $(seq 5)
		do
			hass-cli service call --arguments "entity_id=light.clc${light},brightness={}" light.turn_on &
		done
	)
}

# control panel
MIDI{STATUS==cc}{CC_FUNCTION==74}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]->
{
	eww update light-r={}
	echo {} > ~/.config/midi-macros/state/eww-slider-r
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==75}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]->
{
	eww update light-g={}
	echo {} > ~/.config/midi-macros/state/eww-slider-g
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==76}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE|LOCK=eww_light]->
{
	eww update light-b={}
	echo {} > ~/.config/midi-macros/state/eww-slider-b
	~/.config/midi-macros/scripts/update-lights-eww.py
}
MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> eww update main-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==71}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> eww update cmus-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> eww update focused-volume={}
MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> eww update temperature={}
MIDI{STATUS==cc}{CC_FUNCTION==77}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> eww update brightness={}
MIDI{STATUS==cc}{70<=CC_FUNCTION<=77}(TIME) (python $MM_SCRIPT)[BACKGROUND|INVOCATION_FORMAT=f"{a}\n"]->
{
	import time
	from threading import Thread, Condition
	from subprocess import run, check_output, DEVNULL
	def update_control_panel(is_open):
		run(f'eww {"open" if is_open else "close"} control-panel-window', stdout=DEVNULL, shell=True)
	def control_panel_open():
		return "*" in check_output("eww list-windows | grep control-panel-window", shell=True, text=True)
	def seconds_to_nanos(time_sec):
		return time_sec * 10**9
	def nanos_to_seconds(time_ns):
		return time_ns / 10**9
	def sleep_till(time_ns):
		total_sleep_time = time_ns - time.time_ns()
		if total_sleep_time > 0:
			time.sleep(nanos_to_seconds(total_sleep_time))
	def do_hover():
		last_processed_action_time = None
		while True:
			with new_action_condition:
				new_action_condition.wait_for(lambda: last_action_time != last_processed_action_time)
				last_processed_action_time = last_action_time
			was_control_panel_open = control_panel_open()
			if not was_control_panel_open:
				update_control_panel(True)
			sleep_till(last_processed_action_time + hover_time)
			while True:
				with new_action_condition:
					if last_action_time == last_processed_action_time:
						break
					last_processed_action_time = last_action_time
				sleep_till(last_processed_action_time + hover_time)
			if not was_control_panel_open:
				update_control_panel(False)
	hover_time = seconds_to_nanos(1)
	last_action_time = None
	new_action_condition = Condition()
	Thread(target=do_hover, daemon=True).start()
	while True:
		action_time = int(input())
		with new_action_condition:
			last_action_time = action_time
			new_action_condition.notify()
}
