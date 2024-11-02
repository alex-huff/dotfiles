syntax on
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
set incsearch
set background=dark
let g:gruvbox_italic = 1
let g:gruvbox_contrast_dark = "hard"
let g:gruvbox_contrast_light = "soft"
colorscheme gruvbox
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
nnoremap <Leader>c :execute "edit" fnamemodify(@+, ":~:.")<CR>
nnoremap <Leader>h :nohlsearch<CR>
