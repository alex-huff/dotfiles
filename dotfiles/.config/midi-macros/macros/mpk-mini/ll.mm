MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE>=64} → swaymsg workspace 5
MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE<64} → swaymsg workspace 6
