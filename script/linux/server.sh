#!/bin/bash
source "./script/linux/config.sh"

server_start="${pythonalias} server/app.py"

# this-file.sh -r? / -t? <password>?

if [[ $1 == "-r" ]]; then
    $server_start

# test mode
elif [[ $1 == "-t" ]]; then
    # check for password
    if [[ $2 != "" ]]; then
        server_start="${server_start} -p=$2"
    fi

    # run the commnad & return the process id
    $server_start &
    PID=$!
    echo "$PID" >>"client-pid.txt"
fi