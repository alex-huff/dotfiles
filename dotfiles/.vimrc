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
syntax off
inoremap <nowait> <C-[> <Esc>
cnoremap <nowait> <C-[> <C-\><C-N>
nnoremap <C-h> :wincmd h<CR>
nnoremap <C-j> :wincmd j<CR>
nnoremap <C-k> :wincmd k<CR>
nnoremap <C-l> :wincmd l<CR>
nnoremap <C-S-H> :resize -1<CR>
nnoremap <C-S-L> :resize +1<CR>
nnoremap <Leader>t :silent !dup<CR>:redraw!<CR>
