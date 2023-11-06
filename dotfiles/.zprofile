[[ -f ~/.zshrc ]] && . ~/.zshrc

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]
then
	mv sway.log sway.log.old
	exec sway &> sway.log
fi
