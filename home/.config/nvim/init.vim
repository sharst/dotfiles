" Map the leader key to SPACE
let mapleader="\<SPACE>"

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
if &listchars ==# 'eol:$'
  set listchars=tab:>\ \ \ ,trail:-,extends:>,precedes:<,nbsp:+
endif
set list                " Show problematic characters.

" Also highlight all tabs and trailing whitespace characters.
" highlight ExtraWhitespace ctermbg=darkgreen guibg=darkgreen
" match ExtraWhitespace /\s\+$\|\t/

set ignorecase          " Make searching case insensitive
set smartcase           " ... unless the query has capital letters.
set magic               " Use 'magic' patterns (extended regular expressions).


" Use <C-L> to clear the highlighting of :set hlsearch.
if maparg('<C-L>', 'n') ==# ''
  nnoremap <silent> <C-L> :nohlsearch<CR><C-L>
endif

" Search and Replace
nmap <Leader>s :%s//gc<Left><Left><Left>
" Hit esc to clear last search highlight
nnoremap <silent> <esc> :noh<cr><esc>
hi MatchParen cterm=none ctermbg=none ctermfg=darkblue

" Hide file types from netrw
let g:netrw_list_hide= '.*\.pyc$'

"Custom filetypes
au BufRead,BufNewFile *.launch		    set filetype=xml
au BufRead,BufNewFile *.ino,*.pde       set filetype=cpp
au BufRead,BufNewFile *.html            set filetype=htmlm4

filetype plugin indent on
let g:python_host_prog = '/usr/bin/python'
let g:deoplete#enable_at_startup = 1

let g:ale_sign_error = '✗'
let g:ale_sign_warning = '⚠'
let g:ale_lint_delay = 1000

call plug#begin('~/.config/nvim/plugged')
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
Plug 'davidhalter/jedi-vim'  "python features for vim like jump to definition
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all --no-update-rc --no-completion' } "FZF command line tool
Plug 'junegunn/fzf.vim' "corresponding vim plugin to fzf
Plug 'hynek/vim-python-pep8-indent' "Better intentat for .py files
Plug 'w0rp/ale'
Plug 'lifepillar/vim-solarized8' "
call plug#end()
colorscheme solarized8_dark
