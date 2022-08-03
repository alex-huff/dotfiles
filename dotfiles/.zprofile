#
# ~/.zprofile
#

[[ -f ~/.zshrc ]] && . ~/.zshrc

setxkbmap -option caps:super

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
