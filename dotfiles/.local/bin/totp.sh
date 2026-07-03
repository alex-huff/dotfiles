#!/bin/sh

twofa_dir=~/.2fa
choosen_service=$(find $twofa_dir -type f -regex ".*\.key\.gpg" | sed "s|${twofa_dir}/\(.*\)\.key\.gpg|\1|" | fuzzel --dmenu)
fuzzel --dmenu --password --prompt-only="password: " --width=20 |
    gpg --passphrase-fd=0 --pinentry-mode=loopback --batch --decrypt --no-symkey-cache ${twofa_dir}/"${choosen_service}".key.gpg |
        oathtool --base32 --totp - |
            wl-copy -n
