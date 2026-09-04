#!/bin/sh

jq_build_fzf_item_script=$(
	cat <<-"EOF"
		.[] |
		    select(. != null and .stream != null) |
		        "\(.login)\n\(.broadcastSettings.game.displayName)\n\(.broadcastSettings.title)\n\(.stream.viewersCount)\n\(.stream.previewImageURL)"
	EOF
)

export SMALL_KITTY_OVERLAY=true
export DARK_KITTY_OVERLAY=true
export KITTY_CONF_TWITCH_OVERLAY="placement_strategy top"
twitch-get-channels-json.py < $TWITCH_SUBS_FILE |
    jq --raw-output0 "$jq_build_fzf_item_script" |
        flock --nonblocking /tmp/twitch.sh-lockfile kitty-chooser \
                --layout=reverse \
                --multi \
                --read0 \
                --delimiter="\n" \
                --with-nth="{1}" \
                --accept-nth="{1}" \
                --preview-window="right,65%,border-sharp" \
                --preview="twitch-channel-fzf-preview.sh {2} {3} {4} {5}" |
            twitch-watch-streams.py
