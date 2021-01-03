# ROS SETTINGS
export CMAN_CONFIG_DIR=/opt/magazino/config
export CATKIN_WS=$HOME/catkin_ws
export EDITOR="nvim"
export PYTHONPATH=$PYTHONPATH:$HOME/python_modules

# Magazino Settings
export CATKIN_WS=$HOME/catkin_ws
source $HOME/dotfiles/bash/bashrc_magazino
export DJANGO_SETTINGS_MODULE=toru_django.settings
IS_ROBOT=no
COLOR_PROMPT=yes

alias vi="nvim"
alias dl="youtube-dl -x -f bestaudio[ext=m4a] --audio-format mp3"
ssh-add &> /dev/null
synclient TapButton1=0
source "$HOME/.homesick/repos/homeshick/homeshick.sh"
alias jenkinsroute="ssh -L 8080:10.8.1.41:8080 t26"
alias cal='ncal -wM -3'
# Immediately save bash history on each command
shopt -s histappend
PROMPT_COMMAND="history -a;$PROMPT_COMMAND"
