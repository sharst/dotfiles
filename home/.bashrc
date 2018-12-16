# ROS SETTINGS
export CMAN_CONFIG_DIR=/opt/magazino/config
export ROS_MASTER_URI=http://x250:11311
export ROS_HOSTNAME=x250
export ROS_LOG_DIR=$HOME/workspace/solarbot_ros/logs
export EDITOR="nvim"

# Magazino Settings
export CATKIN_WS=$HOME/catkin_ws
source $HOME/dotfiles/bash/bashrc_magazino
export DJANGO_SETTINGS_MODULE=toru_django.settings
IS_ROBOT=no
COLOR_PROMPT=yes

alias vi="nvim"
alias oh="cd $HOME/workspace/OpenHumidor/"
alias dl="youtube-dl -x --audio-format mp3"
source "$HOME/.homesick/repos/homeshick/homeshick.sh"
ssh-add &> /dev/null
synclient TapButton1=0
