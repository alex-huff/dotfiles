#!/bin/sh

export FZF_DEFAULT_OPTS="
    $FZF_DEFAULT_OPTS
    --layout=reverse
    --multi
    --read0
    --delimiter='\n'
    --with-nth='{1}'
    --accept-nth='{1}'
    --preview-window='right,70%'
    --preview='twitch-channel-fzf-preview.sh {2} {3} {4}'"

jq_build_fzf_item_script=$(
	cat <<-"EOF"
		.[] |
		    select(. != null and .stream != null) |
		        "\(.login)\n\(.stream.title)\n\(.stream.viewersCount)\n\(.stream.previewImageURL)"
	EOF
)
twitch-get-channels-json.py < $TWITCH_SUBS_FILE |
    jq --raw-output0 "$jq_build_fzf_item_script" |
        kitty-chooser |
            twitch-watch-streams.py
