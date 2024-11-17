# 36{c==9} -> mc-cli --pid $(focused-pid.sh) send chat ".pycraft record start"
# 37{c==9} -> mc-cli --pid $(focused-pid.sh) send chat ".pycraft record save latest"
# 38{c==9} -> mc-cli --pid $(focused-pid.sh) send chat ".pycraft run playback_recording.py latest.pcr"
# 39{c==9} -> switch-active-pycraft-recording.sh
# 39+38{c==9} -> mc-cli --pid $(focused-pid.sh) send chat ".pycraft run playback_recording.py active.pcr true"
36{c==9} (python $MM_SCRIPT)[BACKGROUND|INVOCATION_FORMAT=f"{a}\n"]->
{
    import sys
    import time
    import subprocess
    import random
    from threading import Thread, Event

    target_cps = 10
    interval = 1 / target_cps
    random_span = .3 * interval
    random_lower_bound = interval - random_span
    random_upper_bound = interval + random_span

    def left_click(press=True):
        subprocess.run(('swaymsg', 'seat', '-', 'cursor', 'press' if press else 'release', 'button1'))

    def click_forever():
        while not stop_event.is_set():
            start_time = time.time()
            random_interval = random.uniform(random_lower_bound, random_upper_bound)
            half_random_interval = random_interval / 2
            half_random_span = .1 * half_random_interval
            left_click(press=True)
            time.sleep(random.uniform(half_random_interval - half_random_span, half_random_interval + half_random_span))
            left_click(press=False)
            time.sleep(random_interval - (time.time() - start_time))

    enabled = False
    thread = None
    stop_event = Event()
    while True:
        input()
        if enabled:
            stop_event.set()
            thread.join()
            stop_event.clear()
        else:
            thread = Thread(target=click_forever, daemon=True)
            thread.start()
        enabled = not enabled
}
# 37{c==9} -> mc-cli --pid $(focused-pid.sh) send command "fix all"
# 38{c==9} -> mc-cli --pid $(focused-pid.sh) send command "sell all"
D3 MIDI{STATUS==cc}{CC_FUNCTION==70}("{}"->f"{round(CC_VALUE_SCALED(30, 110))}") [BLOCK|DEBOUNCE]->
{
    pid=$(focused-pid.sh)
    mc-cli --pid $pid send chat-local "$(mc-cli --pid $pid set-fov {})"
}
D3 MIDI{STATUS==cc}{CC_FUNCTION==75}("{}"->f"{CC_VALUE_SCALED(0, 1):.2f}") [BLOCK|DEBOUNCE]->
{
    pid=$(focused-pid.sh)
    mc-cli --pid $pid send chat-local "$(mc-cli --pid $pid set-brightness {})"
}
MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"->f"{CC_VALUE_SCALED(0, 1):.2f}") [BLOCK|DEBOUNCE]->
{
    pid=$(focused-pid.sh)
    mc-cli --pid $pid send chat-local "$(mc-cli --pid $pid set-volume {})"
}
# MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE>=64} -> kill -STOP $(ps ax ho pid,command | sed '/[c]osmicpvp/I!d; s/\s*\([0-9]*\).*/\1/')
# MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE<64} -> kill -CONT $(ps ax ho pid,command | sed '/[c]osmicpvp/I!d; s/\s*\([0-9]*\).*/\1/')
MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE>=64} -> mc-cli send command "fix all"
