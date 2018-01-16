# ROS SETTINGS
export CATKIN_WS=$HOME/workspace/solarbot_ros
export CMAN_CONFIG_DIR=/opt/magazino/config
source $HOME/workspace/solarbot_ros/devel/setup.bash
export ROS_WORKSPACE=~/workspace/solarbot_ros
export ROS_MASTER_URI=http://x250:11311
export ROS_HOSTNAME=x250
export ROS_LOG_DIR=$HOME/workspace/solarbot_ros/logs
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$HOME/workspace/solarbot_ros/src
export PATH=$PATH:$HOME/workspace/solarbot_ros/src/solarbot_main/quickscripts
export PYTHONPATH=$PYTHONPATH:$HOME/workspace/
export PYTHONPATH=$PYTHONPATH:$HOME/workspace/solarbot_ros/src/solarbot_main/scripts
export EDITOR="nvim"

# Magazino Settings
source $HOME/dotfiles/bash/bashrc_magazino
IS_ROBOT=no
COLOR_PROMPT=yes

alias vi="nvim"
alias oh="cd $HOME/workspace/OpenHumidor/"
alias hc='chromium-browser --app="http://magazino.hipchat.com/chat" &'
source "$HOME/.homesick/repos/homeshick/homeshick.sh"
ssh-add > /dev/null
synclient TapButton1=0
