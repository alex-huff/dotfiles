#!/bin/sh

uri=$(decode-qrcode-on-screen.sh)
if [ -z $uri ]
then
    exit 1
fi
google_authenticator_json_data=$(echo $uri | extract-google-authenticator-params-from-uris.py | jq ".[0]")
proto=$(echo $google_authenticator_json_data | jq --raw-output ".proto")
label=$(echo $google_authenticator_json_data | jq --raw-output ".label")
if [ "$proto" != "totp" -o -z "$label" ]
then
    exit 1
fi
secret=$(echo $google_authenticator_json_data | jq --raw-output ".parameters.secret[0]")
if [ -z "$secret" ]
then
    exit 1
fi
twofa_dir=~/.2fa
twofa_key_file=$twofa_dir/"$label".key.gpg
echo $secret |
    gpg --yes \
        --output="$twofa_key_file" \
        --passphrase-file=<(fuzzel --dmenu --password --prompt-only="password: " --width=20) \
        --pinentry-mode=loopback \
        --batch \
        --symmetric \
        -
echo $secret |
    oathtool --base32 --totp - |
        wl-copy -n
