36{c==9} →
{
	pid=$(focused-pid.sh)
	mod=$(mod-menu-integration --pid $pid get-mod-names | rofi -dmenu -i -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
	mod-menu-integration --pid $pid open-config "$mod"
}
37{c==9} → mod-menu-integration --pid $(focused-pid.sh) open-config Tweakeroo
38{c==9} → mod-menu-integration --pid $(focused-pid.sh) open-config MiniHUD
