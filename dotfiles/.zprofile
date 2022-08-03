#
# ~/.zprofile
#

[[ -f ~/.zshrc ]] && . ~/.zshrc

setxkbmap -option ctrl:nocaps

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
