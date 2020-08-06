#!/bin/bash

FILE=/tmp/pomodoro-status
DURATION=1500

start_pomodoro () {
    echo "🍅" >> $FILE
    now=$(date +%s)
    end_time=$(($now + $DURATION))
    echo $end_time >> $FILE
    pkill -RTMIN+12 i3blocks
    sleep 5 && notify-send "DUNST_COMMAND_PAUSE"
}

stop_pomodoro () {
    notify-send "DUNST_COMMAND_RESUME"
    rm $FILE
    pkill -RTMIN+12 i3blocks
}

update_pomodoro () {
    now=$(date +%s)
    end_time=$(head -n 3 $FILE | tail -n 1)
    if [[ $now -gt $end_time ]]; then
        notify-send "Pomodoro time's up!"
        stop_pomodoro
        pkill -RTMIN+12 i3blocks
    fi
}

while getopts ":su" opt; do
    case $opt in
        s)
            if [ -f "$FILE" ]; then
                notify-send "Stopping pomodoro"
                stop_pomodoro
            else
                notify-send "Starting pomodoro"
                start_pomodoro
            fi
            ;;
        u)
            if [ -f "$FILE" ]; then
                update_pomodoro
            fi
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done
