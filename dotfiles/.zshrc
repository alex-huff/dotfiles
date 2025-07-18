[[ $- != *i* ]] && return

if [ "$TERM" = linux ]
then
    setvtrgb ~/.config/vt/colors
    clear
fi

setopt INTERACTIVE_COMMENTS
setopt VI
autoload edit-command-line
zle -N edit-command-line
bindkey -M vicmd v edit-command-line

alias cmus="PULSE_SINK=hush cmus"
alias discord="PULSE_SINK=hush discord"

for color in $(color-manager list-colors)
do
    alias fg${color}="color-manager set foreground --by-name $color"
    alias bg${color}="color-manager set background --by-name $color"
done
alias cmcd="color-manager cycle dark"
alias cmcl="color-manager cycle light"

if (( $+CHOOSER ))
then
    alias choose="$CHOOSER"
fi

if (( $+commands[fzf] ))
then
    source <(fzf --zsh)
fi

if (( $+commands[kitty] ))
then
    alias ssh="kitty +kitten ssh"
fi

if (( $+commands[vim] ))
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

PS1='%m$ '

# Rehash pacman command cache when it goes out of date
zshcache_time="$(date +%s%N)"

rehash_precmd()
{
    if [[ -a /var/cache/zsh/pacman ]]
    then
        local paccache_time="$(date -r /var/cache/zsh/pacman +%s%N)"
        if (( zshcache_time < paccache_time )); then
            rehash
            zshcache_time="$paccache_time"
        fi
    fi
}

autoload -Uz add-zsh-hook compinit
add-zsh-hook -Uz precmd rehash_precmd
compinit
zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
fpath=(~/.zsh $fpath)

if (( $+CUSTOM_HISTFILE ))
then
    HISTFILE=$CUSTOM_HISTFILE
else
    HISTFILE=~/.zsh_history
fi
HISTSIZE=100000
SAVEHIST=100000
setopt APPEND_HISTORY
setopt HIST_IGNORE_SPACE
setopt HIST_IGNORE_ALL_DUPS

# source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
# bindkey '^ ' autosuggest-accept

export PYENV_ROOT="$HOME/.pyenv"
if [ -d $PYENV_ROOT/bin ]
then
    path=($PYENV_ROOT/bin $path)
    eval "$(pyenv init -)"
fi
export GOENV_ROOT="$HOME/.goenv"
if [ -d $GOENV_ROOT/bin ]
then
    path=($GOENV_ROOT/bin $path)
    eval "$(goenv init -)"
fi

for file in ~/.zsh/conf.zsh.d/*.zsh(N)
do
    if [ -f $file ]
    then
        source $file
    fi
done
