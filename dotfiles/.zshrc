# Created by newuser for 5.9

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

if command -v lsd &> /dev/null
then
    alias ls="lsd --color=auto"
fi

if command -v bat &> /dev/null
then
    alias cat="bat"
fi

PS1='%F{cyan}%n%F{blue}@%F{cyan}%m%F{default}:%F{blue}%~%F{default}$ '

### CHANGE TITLE OF TERMINALS
case ${TERM} in
  xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|alacritty|st|konsole*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
        ;;
  screen*)
    PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
    ;;
esac

set -o vi

# eval "$(starship init bash)"
