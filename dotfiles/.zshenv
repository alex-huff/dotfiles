typeset -U path PATH
path=(~/.cargo/bin $path)
path=(~/.local/bin $path)
path=(~/.local/share/JetBrains/Toolbox/scripts $path)
export PATH
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=sway
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=lcd'
export MOZ_DBUS_REMOTE=1
export EDITOR=vim
