[[ $- != *i* ]] && return

if command -v nvim &> /dev/null
then
	alias vim=nvim
fi

alias cmus='PULSE_SINK=hush cmus'
alias discord='PULSE_SINK=hear discord'

setopt vi

PS1='[%n@%m]> '

# Rehash pacman command cache when it goes out of date
zshcache_time="$(date +%s%N)"

autoload -Uz add-zsh-hook

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

HISTFILE=~/.zsh_history
HISTSIZE=100000
SAVEHIST=100000
setopt APPEND_HISTORY
setopt HIST_IGNORE_SPACE
setopt HIST_IGNORE_ALL_DUPS

source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
bindkey '^ ' autosuggest-accept

add-zsh-hook -U precmd rehash_precmd

zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
fpath=(~/.zsh $fpath)

autoload -U compinit
compinit

source ~/.zsh/zsh-history-substring-search/zsh-history-substring-search.zsh
bindkey -M vicmd 'k' history-substring-search-up
bindkey -M vicmd 'j' history-substring-search-down

for file in ~/.zsh/conf.zsh.d/*.zsh(N)
do
	if [ -f $file ]
	then
		source $file
	fi
done
