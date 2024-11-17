syntax on
filetype plugin on
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
set nofixendofline
let g:gruvbox_italic = 1
let g:gruvbox_contrast_dark = "hard"
let g:gruvbox_contrast_light = "soft"
colorscheme gruvbox
if &termguicolors
    set list
    set listchars=tab:<->,lead:·,trail:·,multispace:·
endif
try
    packadd comment
catch /^Vim\%((\a\+)\)\?:E919:/
endtry
inoremap <nowait> <C-[> <Esc>
cnoremap <nowait> <C-[> <C-\><C-N>
nnoremap <C-H> :wincmd h<CR>
nnoremap <C-J> :wincmd j<CR>
nnoremap <C-K> :wincmd k<CR>
nnoremap <C-L> :wincmd l<CR>
nnoremap <A-1> 1gt
nnoremap <A-2> 2gt
nnoremap <A-3> 3gt
nnoremap <A-4> 4gt
nnoremap <A-5> 5gt
nnoremap <A-6> 6gt
nnoremap <A-7> 7gt
nnoremap <A-8> 8gt
nnoremap <A-9> 9gt
nnoremap <A-0> 10gt
nnoremap <silent> <C-S-J> :<C-U>execute "move" min([line(".") + v:count1, line("$")])<CR>
nnoremap <silent> <C-S-K> :<C-U>execute "move" max([line(".") - (v:count1 + 1), 0])<CR>
vnoremap <silent> <C-S-J> :<C-U>execute "'<,'>move" min([line("'>") + v:count1, line("$")])<CR>V'<o
vnoremap <silent> <C-S-K> :<C-U>execute "'<,'>move" max([line("'<") - (v:count1 + 1), 0])<CR>V'<o
nnoremap <C-S-H> gT
nnoremap <C-S-L> gt
nnoremap <C-A-J> :resize -1<CR>
nnoremap <C-A-K> :resize +1<CR>
nnoremap <C-A-H> :vertical resize -1<CR>
nnoremap <C-A-L> :vertical resize +1<CR>
nnoremap <Leader>t :botright terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <Leader>T :vertical botright terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <Leader><Leader>t :tab terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <Leader>d :silent !dup<CR>:redraw!<CR>
nnoremap <Leader>c :execute "tabedit" fnamemodify(@+, ":~:.")<CR>
nnoremap <Leader>C :execute "edit" fnamemodify(@+, ":~:.")<CR>
nnoremap <Leader>h :nohlsearch<CR>
nnoremap <Leader>ap :%!autopep8 -<CR>
