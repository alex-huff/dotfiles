#
# ~/.bashrc
#

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

# PS1='[\u@\h \W]\$ '
PS1='\[\e[0;34m\]\w \[\e[0;30m\]>\[\e[0m\] '

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
