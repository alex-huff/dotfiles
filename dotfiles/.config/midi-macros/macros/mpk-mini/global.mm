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

# mute mic with pedal
MIDI{STATUS==cc}{CC_FUNCTION==sustain}("{}"->f"{CC_VALUE >= 64}") [BLOCK|DEBOUNCE]-> pactl set-source-mute $MICROPHONE_SOURCE {} && speak-it <<< "muted {}"

# main volume with knob 1
MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> pactl set-sink-volume $MAIN_SINK {}%

# cmus volume with knob 2
MIDI{STATUS==cc}{CC_FUNCTION==71}("{}"->CC_VALUE_PERCENT) [BLOCK|DEBOUNCE]-> cmus-remote --volume {}%

# control focused application volume with knob 3
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->f"{CC_VALUE_SCALED(0, 1)}") (python)[BLOCK|DEBOUNCE]->
{
    import sys
    from subprocess import check_output
    focused_pid = check_output(
        "focused-pid.sh",
        text=True,
        shell=True
    ).rstrip()
    if focused_pid == "null":
        sys.exit(0)
    focused_pid = int(focused_pid)
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
C3 MIDI{STATUS==cc}{CC_FUNCTION==73}(CC_VALUE_PERCENT) [BACKGROUND|INVOCATION_FORMAT=f"{a}\n"|KILL]->
{
    while true
    do
        ssh alex@lap "xargs -n1 echo > /sys/class/backlight/amdgpu_bl1/brightness"
        sleep 30
    done
}

# cmus
40{c==9} -> cmus-remote --pause
41{c==9} -> cmus-remote --prev
42{c==9} -> cmus-remote --next
43{c==9} -> cmus-remote -C "toggle repeat_current"
MIDI{STATUS==cc}{CC_FUNCTION==74}("{}"->CC_VALUE) [BLOCK|DEBOUNCE]->
{
    current_song_duration=$(cmus-remote -Q | grep duration | cut -d " " -f 2)
    cmus-remote --seek $(python -c "print(round(({} / 127) * $current_song_duration))")
}

# mpv
MIDI{STATUS==pb}("{}"->f"{DATA_2_SCALED(-57/7, 10):.2f}") (python)[BLOCK|DEBOUNCE]->
{
    from subprocess import check_output, run
    import json
    playback_rate = {}
    focused_pid = int(check_output("focused-pid.sh"))
    speed_command = {"command": ["set_property", "speed", abs(playback_rate)]}
    direction_command = {"command": ["set_property", "play-direction", "forward" if playback_rate > 0 else "backward"]}
    display_command = {"command": ["show-text", f"Playback Rate: {playback_rate}"]}
    json_payload = "\n".join(json.dumps(command) for command in (speed_command, direction_command, display_command))
    run(f"echo '{json_payload}' | socat - $XDG_RUNTIME_DIR/mpv-ipc-{focused_pid}.sock", shell=True)
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
    from sys import stdin
    from subprocess import Popen, run, check_output, PIPE, CalledProcessError
    import time
    import threading
    import shutil
    import json
    import websocket as pywebsocket
    import obswebsocket

    def speak(to_speak):
        speech_process = Popen("speak-it", stdin=PIPE, text=True)
        speech_process.stdin.write(to_speak)
        speech_process.stdin.close()

    def save_obs_replay():
        global replay_save_finished
        with replay_save_finished_condition:
            replay_save_finished = False
            succeeded = False
            try:
                succeeded = websocket.call(obswebsocket.requests.SaveReplayBuffer()).status
            except pywebsocket._exceptions.WebSocketException:
                pass
            if not succeeded:
                return False
            return replay_save_finished_condition.wait_for(lambda: replay_save_finished, timeout=20)

    def get_current_timestamp_in_mpv():
        json_result = check_output('echo \'{"command": ["get_property", "playback-time"]}\' | socat - $XDG_RUNTIME_DIR/mpv-ipc-$(focused-pid.sh).sock', shell=True, text=True)
        if not json_result:
            return False, -1
        json_result_object = json.loads(json_result)
        if json_result_object["error"] != "success":
            return False, -1
        return True, json_result_object["data"]

    def open_video_in_mpv(video_path):
        return Popen((mpv_path, "--wayland-app-id=mpv-clipper-dialogue", video_path))

    def clip_video(video_path, beginning_timestamp, end_timestamp):
        duration = end_timestamp - beginning_timestamp
        if duration < 0:
            return False, ""
        try:
            clip_name = check_output('rofi -dmenu -l 0 -p "clip name"', shell=True, text=True).rstrip()
        except CalledProcessError:
            return False, ""
        out_path = os.path.expanduser(f"~/clips/{clip_name}")
        clipper_process = run(("ffmpeg", "-y", "-ss", str(beginning_timestamp), "-i", video_path, "-t", str(duration), "-c:a", "copy", "-c:v", "copy", out_path))
        return clipper_process.returncode == 0, out_path

    def on_replay_saved(event):
        global replay_video_path, replay_save_finished
        with replay_save_finished_condition:
            replay_video_path = event.datain["savedReplayPath"]
            replay_save_finished = True
            replay_save_finished_condition.notify_all()

    websocket_host = "localhost"
    websocket_port = 4455
    websocket_password = os.environ["OBS_WEBSOCKET_PASSWORD"]
    websocket = obswebsocket.obsws(websocket_host, websocket_port, websocket_password, authreconnect=5)
    websocket.register(on_replay_saved, obswebsocket.events.ReplayBufferSaved)
    mpv_path = shutil.which("mpv")
    currently_clipping = False
    beginning_timestamp = end_timestamp = replay_video_path = clipping_mpv_process = None
    replay_save_finished = False
    replay_save_finished_condition = threading.Condition()
    websocket.connect()
    for line in stdin:
        line = line.rstrip()
        match line:
            case "":
                if currently_clipping:
                    clipping_mpv_process.kill()
                    clipping_mpv_process.wait()
                    if None in (beginning_timestamp, end_timestamp):
                        speak("cancelling")
                    else:
                        speak("saving")
                        succeeded, clip_video_path = clip_video(replay_video_path, beginning_timestamp, end_timestamp)
                        speak(f"clipping {'succeeded' if succeeded else 'failed'}")
                        if succeeded:
                            open_video_in_mpv(clip_video_path)
                    beginning_timestamp = end_timestamp = None
                else:
                    succeeded = save_obs_replay()
                    if not succeeded:
                        speak("failed to save replay")
                        continue
                    clipping_mpv_process = open_video_in_mpv(replay_video_path)
                currently_clipping = not currently_clipping
            case "B3" | "D4":
                if not currently_clipping:
                    continue
                currently_setting_beginning_timestamp = line == "B3"
                succeeded, timestamp = get_current_timestamp_in_mpv()
                if succeeded:
                    if currently_setting_beginning_timestamp:
                        beginning_timestamp = timestamp
                    else:
                        end_timestamp = timestamp
                    speak(f"set clip {'beginning' if currently_setting_beginning_timestamp else 'end'}")
                else:
                    speak("could not retrieve timestamp")
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
    : $(
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
C3 MIDI{STATUS==cc}{74<=CC_FUNCTION<=76}(
    f"last_action_time = {TIME}; color[{CC_FUNCTION - 74}] = {round(CC_VALUE_SCALED(0, 255))}\n")
(python $MM_SCRIPT)[BACKGROUND]->
{
    from sys import stdin
    from threading import Thread, Condition
    from subprocess import Popen, DEVNULL

    def do_hass_update():
        last_processed_action_time = None
        while True:
            with new_action_condition:
                new_action_condition.wait_for(lambda: last_action_time != last_processed_action_time)
                color_json = f"[{', '.join(str(component) for component in color)}]"
                last_processed_action_time = last_action_time
            processes = [
                Popen(
                    (
                        "hass-cli",
                        "raw",
                        "ws",
                        "--json",
                        '{"domain":"light","service":"turn_on","service_data":{"entity_id":"light.clc%s","rgb_color":%s}}' % (light, color_json),
                        "call_service"
                    ),
                    stdout=DEVNULL
                ) for light in range(1, 6)
            ]
            for process in processes:
                process.wait()

    last_action_time = None
    new_action_condition = Condition()
    Thread(target=do_hass_update, daemon=True).start()
    color = [0, 0, 0]
    for line in stdin:
        with new_action_condition:
            exec(line)
            new_action_condition.notify_all()
}
C3 MIDI{STATUS==cc}{CC_FUNCTION==77}("{}"->f"{round(CC_VALUE_SCALED(2000, 6500))}") [BLOCK|DEBOUNCE]->
{
    : $(
        for light in $(seq 5)
        do
            hass-cli service call --arguments "entity_id=light.clc${light},kelvin={}" light.turn_on &
        done
    )
}
MIDI{STATUS==cc}{CC_FUNCTION==73}("{}"->f"{round(CC_VALUE_SCALED(0, 255))}") [BLOCK|DEBOUNCE]->
{
    : $(
        for light in $(seq 5)
        do
            hass-cli service call --arguments "entity_id=light.clc${light},brightness={}" light.turn_on &
        done
    )
}

# knobs
* MIDI{STATUS==cc}{70<=CC_FUNCTION<=77}(
    f"last_action_time = {TIME / 10 ** 9}; knob_states[{CC_FUNCTION - 70}] = {CC_VALUE_PERCENT}\n")
(python $MM_SCRIPT)[BACKGROUND]->
{
    from os import path
    from sys import stdin
    from subprocess import run, DEVNULL
    from threading import Thread, Condition
    from json import load, dump
    from time import time, sleep

    def update_knobs_window(is_open):
        run(f"eww {'open' if is_open else 'close'} knobs-window", stdout=DEVNULL, shell=True)

    def is_knobs_window_open():
        return run("eww active-windows | grep knobs-window", stdout=DEVNULL, shell=True).returncode == 0

    def sleep_till(time_seconds):
        total_sleep_time = time_seconds - time()
        if total_sleep_time > 0:
            sleep(total_sleep_time)

    def do_hover():
        last_processed_action_time = None
        while True:
            with new_action_condition:
                new_action_condition.wait_for(lambda: last_action_time != last_processed_action_time)
                last_processed_action_time = last_action_time
            was_knobs_window_open = is_knobs_window_open()
            if not was_knobs_window_open:
                update_knobs_window(True)
            sleep_till(last_processed_action_time + hover_time)
            while True:
                with new_action_condition:
                    if last_action_time == last_processed_action_time:
                        break
                    last_processed_action_time = last_action_time
                sleep_till(last_processed_action_time + hover_time)
            if not was_knobs_window_open:
                update_knobs_window(False)

    def do_update_eww_knobs():
        last_processed_action_time = None
        while True:
            with new_action_condition:
                new_action_condition.wait_for(lambda: last_action_time != last_processed_action_time)
                variables_string = " ".join(f"knob-{i + 1}={state}" for i, state in enumerate(knob_states))
                last_processed_action_time = last_action_time
            run(f"eww update {variables_string}", stdout=DEVNULL, shell=True)

    hover_time = 1
    last_action_time = None
    new_action_condition = Condition()
    Thread(target=do_hover, daemon=True).start()
    Thread(target=do_update_eww_knobs, daemon=True).start()
    knob_state_file_path = path.expanduser("~/.config/midi-macros/state/knobs.json")
    try:
        with open(knob_state_file_path, "r") as knob_state_file:
            knob_states = load(knob_state_file)
    except FileNotFoundError:
        knob_states = [0 for _ in range(8)]
    for line in stdin:
        with new_action_condition:
            exec(line)
            new_action_condition.notify_all()
    with open(knob_state_file_path, "w") as knob_state_file:
        dump(knob_states, knob_state_file)
}

MIDI{STATUS==cc}{CC_FUNCTION==75}("<opacity>"->f"{CC_VALUE_SCALED(0, 1)}")
(swaymsg "`swaymsg -t get_tree | jq -rf $MM_SCRIPT`")[BLOCK|DEBOUNCE|SCRIPT_PATH_AS_ENV_VAR]->
{
    def recurse_nodes: recurse(.floating_nodes[], .nodes[]);
    recurse_nodes |
        select(.focused == true) |
        recurse_nodes |
        select(.pid) |
        "[con_id=\(.id)] opacity <opacity>"
}

MIDI{STATUS==cc}{76<=CC_FUNCTION<=77}(
    "<init>"->f"gap_type={'inner' if CC_FUNCTION==76 else 'outer'}; pixels={CC_VALUE}")
[BLOCK|DEBOUNCE]-> <init>; swaymsg gaps $gap_type current set $pixels

* MIDI{
    (STATUS==pb and
     len(TRIGGER)<2 and
     (not TRIGGER or 48<=TRIGGER[0].getNote()<=51))
}(f"note={TRIGGER[0].getNote()-48 if TRIGGER else None};bend={round(((DATA_2-64)*128+DATA_1)/384)}\n")
(python $MM_SCRIPT)[BACKGROUND]->
{
    import sys
    from subprocess import run
    from time import time, sleep
    from threading import Thread, Lock

    def sleep_till(time_seconds):
        total_sleep_time = time_seconds - time()
        if total_sleep_time > 0:
            sleep(total_sleep_time)

    def manage_window():
        while True:
            start_time = time()
            with lock:
                if should_stop:
                    return
                action = "resize" if is_resize else "move"
                if is_resize:
                    action = "resize"
                    type = "grow" if bend >= 0 else "shrink"
                    dimension = "width" if is_horizontal else "height"
                    modifier = (type, dimension)
                else:
                    action = "move"
                    if is_horizontal:
                        modifier = ("right",) if bend >= 0 else ("left",)
                    else:
                        modifier = ("up",) if bend >= 0 else ("down",)
                amount = (str(abs(bend)), "px")
            swaymsg_command = ("swaymsg", action, *modifier, *amount)
            run(swaymsg_command)
            sleep_till(start_time + .01)

    is_resize = False
    is_horizontal = False
    should_stop = False
    bend = 0
    manage_window_thread = None
    lock = Lock()
    for line in map(str.rstrip, sys.stdin):
        with lock:
            old_bend = bend
            exec(line)
            if note != None:
                is_resize = note < 2
                is_horizontal = note % 2 == 0
            was_bent = old_bend != 0
            is_bent = bend != 0
            if note != None and not was_bent and is_bent:
                manage_window_thread = Thread(target=manage_window)
                manage_window_thread.start()
            elif was_bent and not is_bent:
                should_stop = True
        if should_stop:
            if manage_window_thread:
                manage_window_thread.join()
            should_stop = False
}
