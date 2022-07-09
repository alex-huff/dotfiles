#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

export PATH=~/".pfetch:$PATH"
export PATH=~/".cargo/bin:$PATH"
export PATH=~/".local/bin:$PATH"
export QT_QPA_PLATFORMTHEME="gtk2"
export BAT_THEME="Catppuccin"

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
