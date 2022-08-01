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

set -o vi

# Rehash pacman command cache when it goes out of date
zshcache_time="$(date +%s%N)"

autoload -Uz add-zsh-hook

rehash_precmd() 
{
    if [[ -a /var/cache/zsh/pacman ]]; then
      local paccache_time="$(date -r /var/cache/zsh/pacman +%s%N)"
      if (( zshcache_time < paccache_time )); then
        rehash
        zshcache_time="$paccache_time"
      fi
    fi
}

source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

add-zsh-hook -Uz precmd rehash_precmd

zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
fpath=(~/.zsh $fpath)

autoload -Uz compinit vcs_info
compinit

precmd()
{
    vcs_info
}

# Format the vcs_info_msg_0_ variable
zstyle ':vcs_info:git:*' formats ' %F{cyan}on %F{blue} %F{cyan}%b'
 
# Set up the prompt (with git branch name)
setopt PROMPT_SUBST
PS1='%F{blue}%~${vcs_info_msg_0_} %F{black}>%F{default} '

# eval "$(starship init bash)"
