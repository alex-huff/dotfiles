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
set title
set laststatus=0
set background=dark
set incsearch
if &termguicolors
    set list
    set listchars=tab:<->,lead:·,trail:·,multispace:·
endif
inoremap <nowait> <C-[> <Esc>
cnoremap <nowait> <C-[> <C-\><C-N>
nnoremap <C-h> :wincmd h<CR>
nnoremap <C-j> :wincmd j<CR>
nnoremap <C-k> :wincmd k<CR>
nnoremap <C-l> :wincmd l<CR>
nnoremap <C-S-H> gT
nnoremap <C-S-L> gt
nnoremap <C-A-J> :resize -1<CR>
nnoremap <C-A-K> :resize +1<CR>
nnoremap <C-A-H> :vertical resize -1<CR>
nnoremap <C-A-L> :vertical resize +1<CR>
nnoremap <Leader>t :botright term<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <Leader>T :vertical botright term<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <Leader>d :silent !dup<CR>:redraw!<CR>
nnoremap ,/ :nohlsearch<CR>
hi Cursor       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=NONE      cterm=NONE
hi IncSearch    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi Search       guifg=#000000 guibg=#FABD2F ctermfg=black ctermbg=yellow gui=ITALIC    cterm=NONE
hi CurSearch    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi Visual       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi VisualNOS    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi CursorColumn guifg=#000000 guibg=#FFFFFF ctermfg=grey  ctermbg=white  gui=NONE      cterm=NONE
hi CursorLine   guifg=#000000 guibg=#FFFFFF ctermfg=grey  ctermbg=white  gui=NONE      cterm=NONE
hi Comment      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi DiffChange   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi DiffDelete   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi DiffText     guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Directory    guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Error        guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Folded       guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Function     guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Identifier   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Ignore       guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Label        guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi LineNr       guifg=#665C54 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi MatchParen   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi ModeMsg      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi MoreMsg      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi NonText      guifg=#504945 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Normal       guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PmenuSbar    guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PmenuSel     guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi PmenuThumb   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PreProc      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Special      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi SpecialKey   guifg=#504945 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi Statement    guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi StatusLine   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi StatusLineNC guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi StorageClass guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Structure    guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi TabLine      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi TabLineFill  guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi TabLineSel   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Title        guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Todo         guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Todo         guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=UNDERLINE cterm=UNDERLINE
hi Type         guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi TypeDef      guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Underlined   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=UNDERLINE cterm=UNDERLINE
hi VertSplit    guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi WarningMsg   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi WildMenu     guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi cucumberTags guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi htmlTagN     guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi rubySymbol   guifg=#EBDBB2 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Constant     guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi DiffAdd      guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi Number       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi Pmenu        guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=BOLD      cterm=BOLD
hi String       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
