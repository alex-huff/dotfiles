typeset -U path PATH
path=(~/go/bin ~/go/*/bin(N) $path)
path=(~/.cargo/bin $path)
path=(~/.local/bin $path)
path=(~/.local/share/JetBrains/Toolbox/scripts $path)
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=sway
export PYTHON_BASIC_REPL=1
export GTK_USE_PORTAL=1
export MOZ_DBUS_REMOTE=1
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS=-Dawt.useSystemAAFontSettings=lcd
export EDITOR=vim
export FZF_DEFAULT_OPTS="--preview-window=border-sharp --highlight-line --color=light,gutter:#d5c4a1,current-bg:0,prompt:7,pointer:7,gap-line:7,scrollbar:7,separator:7,preview-border:7"
export MANPAGER='nvim +Man!'
