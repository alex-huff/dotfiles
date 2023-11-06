[[ -f ~/.zshrc ]] && . ~/.zshrc

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]
then
	mv sway.log sway.log.old
	exec dbus-launch --sh-syntax --exit-with-session sway &> sway.log
fi
