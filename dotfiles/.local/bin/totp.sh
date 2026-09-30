#!/bin/sh

twofa_dir=~/.2fa
choosen_service=$(find $twofa_dir -type f -regex ".*\.key\.gpg" | sed "s|${twofa_dir}/\(.*\)\.key\.gpg|\1|" | KITTY_OVERLAY_DIMENSIONS=10:40 kitty-chooser --prompt="service: " --layout=reverse)
if [ -z "$choosen_service" ]
then
    exit 1
fi
fuzzel --dmenu --password --prompt-only="password: " --width=20 |
    gpg --passphrase-fd=0 --pinentry-mode=loopback --batch --decrypt --no-symkey-cache ${twofa_dir}/"${choosen_service}".key.gpg |
        oathtool --base32 --totp - |
            wl-copy -n
