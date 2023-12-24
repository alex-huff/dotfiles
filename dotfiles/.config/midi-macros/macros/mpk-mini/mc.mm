36{c==9} → mc-cli --pid $(focused-pid.sh) send chat ".pycraft record start"
37{c==9} → mc-cli --pid $(focused-pid.sh) send chat ".pycraft record save latest"
38{c==9} → mc-cli --pid $(focused-pid.sh) send chat ".pycraft run playback_recording.py latest.pcr"
39{c==9} → switch-active-pycraft-recording.sh
39+38{c==9} → mc-cli --pid $(focused-pid.sh) send chat ".pycraft run playback_recording.py active.pcr true"
D3 MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"→f"{round(CC_VALUE_SCALED(30, 110))}") [BLOCK|DEBOUNCE]→
{
	pid=$(focused-pid.sh)
	mc-cli --pid $pid send chat-local "$(mc-cli --pid $pid set-fov {})"
}
D3+E3 MIDI{STATUS==cc}{CC_FUNCTION==72}("{}"→f"{CC_VALUE_SCALED(0, 1)}") [BLOCK|DEBOUNCE]→
{
	pid=$(focused-pid.sh)
	mc-cli --pid $pid send chat-local "$(mc-cli --pid $pid set-brightness {})"
}
