36{c==9} → open-mc-mod-configuration.sh
37{c==9} → mc-cli --pid $(focused-pid.sh) open-config Tweakeroo
38{c==9} → mc-cli --pid $(focused-pid.sh) open-config MiniHUD
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
