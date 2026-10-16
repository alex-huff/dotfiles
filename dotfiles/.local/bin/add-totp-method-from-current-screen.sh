#!/bin/bash

uri=$(decode-qrcode-on-screen.sh)
if [ -z "$uri" ]
then
    exit 1
fi

google_authenticator_json_data=$(printf "%s" "$uri" | extract-google-authenticator-params-from-uris.py | jq ".[0]")
proto=$(printf "%s" "$google_authenticator_json_data" | jq --raw-output ".proto")
label=$(printf "%s" "$google_authenticator_json_data" | jq --raw-output ".label")
if [ "$proto" != "totp" -o -z "$label" ]
then
    exit 1
fi

secret=$(printf "%s" "$google_authenticator_json_data" | jq --raw-output ".parameters.secret[0]")
if [ -z "$secret" ]
then
    exit 1
fi

twofa_dir=~/.2fa
twofa_key_file="${twofa_dir}/${label}.key.gpg"
password=$(KITTY_OVERLAY_DIMENSIONS=1:30 kitty-overlay-piped password-prompt)
printf "%s" "$secret" |
    gpg --yes \
        --output="$twofa_key_file" \
        --passphrase-file=<(printf "%s" "$password") \
        --pinentry-mode=loopback \
        --batch \
        --symmetric \
        -
printf "%s" "$secret" |
    oathtool --base32 --totp - |
        wl-copy -n
