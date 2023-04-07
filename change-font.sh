#!/bin/sh

from='RecMonoCasual Nerd Font'
to='VictorMono Nerd Font Mono'

find dotfiles -type f -exec file {} + | awk -F: '/ASCII text/ { print $1 }
                                                 /JSON text data/ { print $1 }
                                                 /Unicode text, UTF-8 text/ { print $1 }' | \
xargs -d '\n' sed -i "s/$from/$to/g"
