36{c==9} →
{
	mod=$(mod-menu-integration get-mod-names | rofi -dmenu -theme ~/.config/rofi/launchers/type-1/style-5.rasi)
	mod-menu-integration open-config $mod
}
37{c==9} → mod-menu-integration open-config litematica
38{c==9} → mod-menu-integration open-config tweakeroo
