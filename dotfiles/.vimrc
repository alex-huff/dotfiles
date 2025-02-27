syntax on
filetype plugin on
set lazyredraw
set termguicolors
set nowrap
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
if has("gui_running")
    set guioptions-=T
    set guioptions-=m
    set guioptions-=L
    set guioptions-=r
    if has("gui_gtk")
        set guifont=Adwaita\ Mono\ 18
    elseif has("gui_win32")
        set guifont=Adwaita_Mono:h18
    endif
endif
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
nnoremap <silent> <C-H> :wincmd h<CR>
nnoremap <silent> <C-J> :wincmd j<CR>
nnoremap <silent> <C-K> :wincmd k<CR>
nnoremap <silent> <C-L> :wincmd l<CR>
nnoremap <silent> <A-n> :cnext<CR>
nnoremap <silent> <A-p> :cprevious<CR>
nnoremap <A-h> zH
nnoremap <A-l> zL
nnoremap <silent> <A-j> :execute "move" min([line(".") + v:count1, line("$")])<CR>
nnoremap <silent> <A-k> :execute "move" max([line(".") - (v:count1 + 1), 0])<CR>
inoremap <silent> <A-j> <Esc>:execute "move" min([line(".") + v:count1, line("$")])<CR>gi
inoremap <silent> <A-k> <Esc>:execute "move" max([line(".") - (v:count1 + 1), 0])<CR>gi
vnoremap <silent> <A-j> :<C-U>silent execute "'<,'>move" min([line("'>") + v:count1, line("$")])<CR>gv
vnoremap <silent> <A-k> :<C-U>silent execute "'<,'>move" max([line("'<") - (v:count1 + 1), 0])<CR>gv
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
nnoremap <C-S-H> gT
nnoremap <C-S-L> gt
nnoremap <silent> <C-S-W> :tabclose<CR>
nnoremap <silent> <C-A-J> :resize -1<CR>
nnoremap <silent> <C-A-K> :resize +1<CR>
nnoremap <silent> <C-A-H> :vertical resize -1<CR>
nnoremap <silent> <C-A-L> :vertical resize +1<CR>
nnoremap <silent> <Leader>t :botright terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <silent> <Leader>T :vertical botright terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <silent> <Leader><Leader>t :tab terminal<CR><C-\><C-N>:set nonumber norelativenumber<CR>a
nnoremap <silent> <Leader>c :execute "tabedit" fnameescape(fnamemodify(@+, ":~:."))<CR>
nnoremap <silent> <Leader>C :execute "edit" fnameescape(fnamemodify(@+, ":~:."))<CR>
nnoremap <silent> <Leader>h :nohlsearch<CR>
nnoremap <silent> <Leader>ap :%!autopep8 -<CR>
