syntax off
set termguicolors
set number
set relativenumber
set ignorecase
set autoindent
set smarttab
set expandtab
set tabstop=4
set shiftwidth=0
set list
set listchars=tab:>~
set title
set laststatus=0
set background=dark
set incsearch
inoremap <nowait> <C-[> <Esc>
cnoremap <nowait> <C-[> <C-\><C-N>
nnoremap <C-h> :wincmd h<CR>
nnoremap <C-j> :wincmd j<CR>
nnoremap <C-k> :wincmd k<CR>
nnoremap <C-l> :wincmd l<CR>
nnoremap <C-S-H> :resize -1<CR>
nnoremap <C-S-L> :resize +1<CR>
nnoremap <Leader>t :silent !dup<CR>:redraw!<CR>
nnoremap ,/ :nohlsearch<CR>
hi Cursor       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white gui=NONE      cterm=NONE
hi IncSearch    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white gui=ITALIC    cterm=NONE
hi Search       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white gui=ITALIC    cterm=NONE
hi Visual       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white gui=ITALIC    cterm=NONE
hi VisualNOS    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white gui=ITALIC    cterm=NONE
hi CursorColumn guifg=#A0A0A0 guibg=#FFFFFF ctermfg=grey  ctermbg=white gui=NONE      cterm=NONE
hi CursorLine   guifg=#A0A0A0 guibg=#FFFFFF ctermfg=grey  ctermbg=white gui=NONE      cterm=NONE
hi Comment      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=ITALIC    cterm=NONE
hi DiffChange   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi DiffDelete   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi DiffText     guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Directory    guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Error        guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Folded       guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Function     guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Identifier   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Ignore       guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Label        guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi LineNr       guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi MatchParen   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi ModeMsg      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi MoreMsg      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi NonText      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Normal       guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi PmenuSbar    guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi PmenuSel     guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=ITALIC    cterm=NONE
hi PmenuThumb   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi PreProc      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Special      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi SpecialKey   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=ITALIC    cterm=NONE
hi Statement    guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi StatusLine   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi StatusLineNC guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=ITALIC    cterm=NONE
hi StorageClass guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Structure    guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi TabLine      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi TabLineFill  guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi TabLineSel   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Title        guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Todo         guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Todo         guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=UNDERLINE cterm=UNDERLINE
hi Type         guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi TypeDef      guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi Underlined   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=UNDERLINE cterm=UNDERLINE
hi VertSplit    guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi WarningMsg   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi WildMenu     guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi cucumberTags guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi htmlTagN     guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=BOLD      cterm=BOLD
hi rubySymbol   guifg=#A0A0A0 guibg=#000000 ctermfg=grey  ctermbg=black gui=NONE      cterm=NONE
hi Constant     guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black gui=NONE      cterm=NONE
hi DiffAdd      guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black gui=NONE      cterm=NONE
hi Number       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black gui=NONE      cterm=NONE
hi Pmenu        guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black gui=BOLD      cterm=BOLD
hi String       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black gui=NONE      cterm=NONE
