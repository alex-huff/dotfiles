typeset -U path PATH
path=(~/.pfetch $path)
path=(~/.cargo/bin $path)
path=(~/.local/bin $path)
path=(~/.local/share/JetBrains/Toolbox/scripts $path)
if command -v pyenv &> /dev/null
then
    export PYENV_ROOT="$HOME/.pyenv"
    [ -d $PYENV_ROOT/bin ] && path=($PYENV_ROOT/bin $path)
    eval "$(pyenv init -)"
fi
export PATH
export QT_QPA_PLATFORM=wayland
export XDG_CURRENT_DESKTOP=sway
export _JAVA_AWT_WM_NONREPARENTING=1
export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=lcd'
export MOZ_DBUS_REMOTE=1
if command -v nvim &> /dev/null
then
    export MANPAGER='nvim +Man!'
    EDITOR=nvim
else
    EDITOR=vim
fi
export EDITOR
