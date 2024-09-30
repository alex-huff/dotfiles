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
nnoremap <C-S-H> :resize -1<CR>
nnoremap <C-S-L> :resize +1<CR>
nnoremap <Leader>t :silent !dup<CR>:redraw!<CR>
nnoremap ,/ :nohlsearch<CR>
hi Cursor       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=NONE      cterm=NONE
hi IncSearch    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi Search       guifg=#000000 guibg=#FABD2F ctermfg=black ctermbg=yellow gui=ITALIC    cterm=NONE
hi CurSearch    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi Visual       guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi VisualNOS    guifg=#000000 guibg=#FFFFFF ctermfg=black ctermbg=white  gui=ITALIC    cterm=NONE
hi CursorColumn guifg=#000000 guibg=#FFFFFF ctermfg=grey  ctermbg=white  gui=NONE      cterm=NONE
hi CursorLine   guifg=#000000 guibg=#FFFFFF ctermfg=grey  ctermbg=white  gui=NONE      cterm=NONE
hi Comment      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi DiffChange   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi DiffDelete   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi DiffText     guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Directory    guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Error        guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Folded       guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Function     guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Identifier   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Ignore       guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Label        guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi LineNr       guifg=#665C54 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi MatchParen   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi ModeMsg      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi MoreMsg      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi NonText      guifg=#504945 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Normal       guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PmenuSbar    guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PmenuSel     guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi PmenuThumb   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi PreProc      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Special      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi SpecialKey   guifg=#504945 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi Statement    guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi StatusLine   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi StatusLineNC guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=ITALIC    cterm=NONE
hi StorageClass guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Structure    guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi TabLine      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi TabLineFill  guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi TabLineSel   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Title        guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Todo         guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Todo         guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=UNDERLINE cterm=UNDERLINE
hi Type         guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi TypeDef      guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi Underlined   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=UNDERLINE cterm=UNDERLINE
hi VertSplit    guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi WarningMsg   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi WildMenu     guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi cucumberTags guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi htmlTagN     guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=BOLD      cterm=BOLD
hi rubySymbol   guifg=#FBF1C7 guibg=#000000 ctermfg=grey  ctermbg=black  gui=NONE      cterm=NONE
hi Constant     guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi DiffAdd      guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi Number       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
hi Pmenu        guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=BOLD      cterm=BOLD
hi String       guifg=#FFFFFF guibg=#000000 ctermfg=white ctermbg=black  gui=NONE      cterm=NONE
