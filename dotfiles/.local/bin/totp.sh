#!/bin/sh

twofa_dir=~/.2fa
choosen_service=$(find $twofa_dir -type f -regex ".*\.key\.gpg" | sed "s|${twofa_dir}/\(.*\)\.key\.gpg|\1|" | rofi -dmenu -i)
gpg --decrypt --no-symkey-cache ${twofa_dir}/"${choosen_service}".key.gpg | oathtool --base32 --totp - | wl-copy -n
