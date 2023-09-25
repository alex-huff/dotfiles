[[ $- != *i* ]] && return

if command -v lsd &> /dev/null
then
	alias ls="lsd --color=auto"
fi

if command -v bat &> /dev/null
then
	alias cat=bat
fi

alias cmus='PULSE_SINK=hush cmus'
alias discord='PULSE_SINK=hear discord'

set -o vi

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
setopt appendhistory

source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
bindkey '^ ' autosuggest-accept

add-zsh-hook -Uz precmd rehash_precmd

zstyle ':completion:*:*:git:*' script ~/.zsh/git-completion.bash
fpath=(~/.zsh $fpath)

autoload -Uz compinit vcs_info
compinit

precmd()
{
	vcs_info
}

zstyle ':vcs_info:git:*' formats ' %F{cyan}on %F{blue} %F{cyan}%b'
setopt PROMPT_SUBST
PS1='%F{blue}%~${vcs_info_msg_0_} %F{black}>%F{default} '

source ~/.zsh/theming/zsh-syntax-highlighting/themes/catppuccin_mocha-zsh-syntax-highlighting.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

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
