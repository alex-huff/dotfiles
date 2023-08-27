[[ $- != *i* ]] && return

if command -v lsd &> /dev/null
then
	alias ls="lsd --color=auto"
fi

if command -v bat &> /dev/null
then
	alias cat="bat"
fi

PS1='\[\e[0;34m\]\w \[\e[0;30m\]>\[\e[0m\] '

set -o vi
