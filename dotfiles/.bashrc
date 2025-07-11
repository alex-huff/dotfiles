[[ $- != *i* ]] && return

if [ "$TERM" = linux ]
then
    setvtrgb ~/.config/vt/colors
    clear
fi

set -o vi
HISTCONTROL=ignoreboth:erasedups

alias cmus="PULSE_SINK=hush cmus"
alias discord="PULSE_SINK=hush discord"

for color in $(color-manager list-colors)
do
    alias fg${color}="color-manager set foreground --by-name $color"
    alias bg${color}="color-manager set background --by-name $color"
done
alias cmcd="color-manager cycle dark"
alias cmcl="color-manager cycle light"

if [ ! -z ${CHOOSER+_} ]
then
    alias choose="$CHOOSER"
fi

if command -v fzf &> /dev/null
then
    source <(fzf --bash)
fi

if command -v kitty &> /dev/null
then
    alias ssh="kitty +kitten ssh"
fi

if command -v vim &> /dev/null
then
    EDITOR=vim
else
    EDITOR=vi
fi
export EDITOR
alias vi="$EDITOR"

alias rg="rg --color=always --hyperlink-format=kitty --column --line-number --no-heading"
alias ls="ls --hyperlink=auto"

alias ff="fzf-find-files"
alias fr="rg-fzf"

PS1='\h$ '

export PYENV_ROOT="$HOME/.pyenv"
if [ -d $PYENV_ROOT/bin ]
then
    PATH="$PYENV_ROOT/bin:$PATH"
    export PATH
    eval "$(pyenv init -)"
fi
export GOENV_ROOT="$HOME/.goenv"
if [ -d $GOENV_ROOT/bin ]
then
    PATH="$GOENV_ROOT/bin:$PATH"
    export PATH
    eval "$(goenv init -)"
fi

shopt -s nullglob
for file in ~/.bash/conf.bash.d/*.bash
do
    if [ -f $file ]
    then
        source $file
    fi
done
