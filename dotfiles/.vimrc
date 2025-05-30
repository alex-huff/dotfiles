syntax off
filetype plugin on
set lazyredraw
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
set nofixendofline
set background=light
if (&term != "linux" && &term != "tmux-256color") || has("gui_running")
    set termguicolors
    set list
    set listchars=tab:<->,lead:·,trail:·,multispace:·
    let g:gruvbox_italic = 1
    let g:gruvbox_contrast_dark = "hard"
    let g:gruvbox_contrast_light = "hard"
    colorscheme gruvbox
    let g:terminal_ansi_colors = ["#ebdbb2", "#cc241d", "#98971a", "#d79921", "#458588", "#b16286", "#689d6a", "#7c6f64", "#928374", "#9d0006", "#79740e", "#b57614", "#076678", "#8f3f71", "#427b58", "#282828"]
    highlight Terminal guibg=#f9f5d7 guifg=#3c3836
endif
if has("gui_running")
    set guioptions-=T
    set guioptions-=m
    set guioptions-=L
    set guioptions-=r
    if has("gui_gtk")
        set guifont=Fira\ Code\ 18
    elseif has("gui_win32")
        set guifont=Fira_Code:h18
    endif
endif
try
    packadd comment
catch /^Vim\%((\a\+)\)\?:E919:/
endtry
function s:save_location_to_clipboard()
    let [bufnum, lnum, col, off, curswant] = getcurpos()
    let start_of_line_offset = line2byte(lnum)
    let @+ = $"{fnamemodify(@%, ":p")}:{start_of_line_offset + (col - 1)}"
endfunction
function s:jump_to_clipboard_location(open_cmd)
    let separator_idx = match(@+, ":\\d\\+$")
    let file_path = @+[0:separator_idx - 1]
    let byte_offset = @+[separator_idx + 1:]
    execute a:open_cmd fnameescape(fnamemodify(file_path, ":~:."))
    execute "goto" byte_offset
    normal! zz
endfunction
function s:do_ruff_format(original_cursor, use_range=v:false, start_line=1, end_line=1, start_column=1, end_column=1)
    " Do a 'fake' change so that undo restores cursor position correctly. This
    " is needed because undoing a filter restores cursor position to the start
    " of the range filtered instead of where the cursor was before the filter
    " took place. Since 'i_' and 'x' are considered a change and are executed
    " before the filter, when undoing a 'do_ruff_format' invocation the cursor
    " is correctly restored to the position before this fake change.
    normal! i_
    normal! x
    let range_specifier = ""
    if a:use_range
        let range_start_specifier = $"{a:start_line}:{a:start_column}"
        let range_end_specifier = $"{a:end_line}:{a:end_column}"
        let range_specifier = $" --range={range_start_specifier}-{range_end_specifier}"
    endif
    execute $"%!ruff format -{range_specifier}"
    call setcursorcharpos(a:original_cursor[1:])
endfunction
function s:ruff_format_operatorfunc(original_cursor, type)
    if a:type == "block"
        return
    endif
    let [_, start_line, start_column, _] = getcharpos("'[")
    let [_, end_line, end_column, _] = getcharpos("']")
    let is_line = a:type == "line"
    call s:do_ruff_format(a:original_cursor, v:true, start_line, end_line + (is_line ? 1 : 0), (is_line ? 1 : start_column), (is_line ? 1 : end_column + 1))
endfunction
function s:setup_ruff_format_operatorfunc()
    let original_cursor = getcursorcharpos()
    let &operatorfunc = { type -> s:ruff_format_operatorfunc(original_cursor, type) }
    return "g@"
endfunction
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
nnoremap <silent> <Leader>c :call <SID>jump_to_clipboard_location("tabedit")<CR>
nnoremap <silent> <Leader>C :call <SID>jump_to_clipboard_location("edit")<CR>
nnoremap <silent> <C-Space> :call <SID>save_location_to_clipboard()<CR>
nnoremap <silent> <Leader>h :nohlsearch<CR>
nnoremap <silent> <Leader>gb :call <SID>do_ruff_format(getcursorcharpos())<CR>
nnoremap <silent> <expr> gb <SID>setup_ruff_format_operatorfunc()
vnoremap <silent> <expr> gb <SID>setup_ruff_format_operatorfunc()
nnoremap <silent> <expr> gbb <SID>setup_ruff_format_operatorfunc() .. "_"
nnoremap <silent> <Leader>f :FZF<CR>
