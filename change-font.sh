#!/bin/sh

from='ComicCodeLigatures Nerd Font Mono'
to='ComicCode Nerd Font'

find dotfiles -type f -exec file {} + | awk -F: '/ASCII text/ { print $1 }
                                                 /JSON text data/ { print $1 }
                                                 /Unicode text, UTF-8 text/ { print $1 }' | \
xargs -d '\n' sed -i "s/$from/$to/g"
