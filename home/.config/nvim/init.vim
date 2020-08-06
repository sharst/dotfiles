" Map the leader key to SPACE 
let mapleader="\<SPACE>"

set encoding=utf-8      " UTF8 as default encoding
set showcmd             " Show (partial) command in status line.
set showmatch           " Show matching brackets.
set showmode            " Show current mode.
set ruler               " Show the line and column numbers of the cursor.
set number              " Show the line numbers on the left side.
set formatoptions+=o    " Continue comment marker in new lines.
set textwidth=0         " Hard-wrap long lines as you type them.
set expandtab           " Insert spaces when TAB is pressed.
set tabstop=2           " Render TABs using this many spaces.
set shiftwidth=2        " Indentation amount for < and > commands.
set nowrap              " Do not wrap text

set noerrorbells        " No beeps.
set modeline            " Enable modeline.
set linespace=0         " Set line-spacing to minimum.
set nojoinspaces        " Prevents inserting two spaces after punctuation on a join (J)

set wildignore+=*.o,*.obj,.git,*.pyc "Ignore stupid files
set colorcolumn=80 "Add a colored line after at 80 characters

" More natural splits
set splitbelow          " Horizontal split below current.
set splitright          " Vertical split to right of current.

if !&scrolloff
  set scrolloff=3       " Show next 3 lines while scrolling.
endif

if !&sidescrolloff
  set sidescrolloff=5   " Show next 5 columns while side-scrolling.
endif
set nostartofline       " Do not jump to first character with page commands.

" Tell Vim which characters to show for expanded TABs,
" trailing whitespace, and end-of-lines. VERY useful!
set list listchars=tab:>\ ,trail:·,extends:>,precedes:<,nbsp:+

set ignorecase          " Make searching case insensitive
set smartcase           " ... unless the query has capital letters.
set magic               " Use 'magic' patterns (extended regular expressions).
set termguicolors

set hidden

"split navigations
nnoremap <C-J> <C-W><C-J>    
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Search and Replace
nmap <Leader>s :%s//gc<Left><Left><Left>
" Hit esc to clear last search highlight
nnoremap <silent> <esc> :noh<cr><esc>

nnoremap <silent> <Leader>b :TagbarToggle<CR>

" Some things I often type wrong, and I don't need editor mode
:cabbrev W w
:cabbrev Wq wq

hi MatchParen cterm=none ctermbg=none ctermfg=darkblue

" Hide file types from netrw
let g:netrw_list_hide= '.*\.pyc$'

"Custom filetypes
au BufRead,BufNewFile *.launch		    set filetype=xml
au BufRead,BufNewFile *.ino,*.pde       set filetype=cpp
au BufRead,BufNewFile *.html            set filetype=htmlm4

filetype plugin indent on
let g:python_host_prog = '/usr/bin/python'
"let g:deoplete#enable_at_startup = 1

let g:ale_sign_error = '✗'
let g:ale_sign_warning = '⚠'
let g:ale_lint_delay = 300

" Disable bracketing paste
set t_BE=

call plug#begin('~/.config/nvim/plugged')
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
" Plug 'davidhalter/jedi-vim'  "python features for vim like jump to definition
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all --no-update-rc --no-completion' } "FZF command line tool
Plug 'junegunn/fzf.vim' "corresponding vim plugin to fzf
Plug 'hynek/vim-python-pep8-indent' "Better intentat for .py files
"Plug 'dense-analysis/ale'
Plug 'lifepillar/vim-solarized8'
Plug 'majutsushi/tagbar'
Plug 'Valloric/YouCompleteMe', { 'do': './install.py' }
Plug 'fisadev/vim-isort'
call plug#end()
colorscheme solarized8_dark
"let g:solarized_use16 = 1

" Open split right or left
nnoremap <leader>l :vsp<CR>:Files<CR>
nnoremap <leader>h :rightb<space>vsp<CR><C-w>h:Files<CR>
nnoremap <leader>j :sp<CR>:Files<CR>

let g:ycm_autoclose_preview_window_after_completion=1
map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>
let g:vim_isort_map = '<C-i>'

let python_highlight_all=1

let g:jedi#show_call_signatures=0

" FZF config
let g:fzf_nvim_statusline = 0 " disable statusline overwriting
nnoremap <silent><leader>f :Files<CR>
" The Silver Searcher
if executable('ag')
  " Use ag over grep
  set grepprg=ag\ --nogroup\ --nocolor
endif

" bind K to grep word under cursor
nnoremap <silent> K :grep! "\b<C-R><C-W>\b"<CR>:cw<CR>


" Setting ipdb breakponts
python << EOF
import vim
import re

ipdb_breakpoint = 'import ipdb; ipdb.set_trace()'

def set_breakpoint():
    breakpoint_line = int(vim.eval('line(".")')) - 1

    current_line = vim.current.line
    white_spaces = re.search('^(\s*)', current_line).group(1)

    vim.current.buffer.append(white_spaces + ipdb_breakpoint, breakpoint_line)

def remove_breakpoints():
    op = 'g/^.*%s.*/d' % ipdb_breakpoint
    vim.command(op)

def toggle_breakpoint():
    breakpoint_line = int(vim.eval('line(".")')) - 1
    if 'import ipdb; ipdb.set_trace()' in vim.current.buffer[breakpoint_line]:
        remove_breakpoints()
    elif 'import ipdb; ipdb.set_trace()' in vim.current.buffer[breakpoint_line-1]:
        remove_breakpoints()
    else :
        set_breakpoint()
    vim.command(':w')

vim.command('map <f6> :py toggle_breakpoint()<cr>')
EOF

