typeset -U path PATH
path=(~/.pfetch $path)
path=(~/.cargo/bin $path)
path=(~/.local/bin $path)
path=(~/screenshots $path)
path=(~/.local/share/JetBrains/Toolbox/scripts $path)
export PATH
export QT_QPA_PLATFORMTHEME=qt5ct:qt6ct
export BAT_THEME=Catppuccin
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=sway
export _JAVA_AWT_WM_NONREPARENTING=1
export MOZ_DBUS_REMOTE=1
export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=lcd'
if command -v nvim &> /dev/null
then
	export MANPAGER='nvim +Man!'
	EDITOR=nvim
else
	EDITOR=vim
fi
export EDITOR
