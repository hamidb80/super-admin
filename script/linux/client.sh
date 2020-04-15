#!/bin/bash
source "./script/linux/config.sh"

client_start="${pythonalias} client/app.py"
# this-file.sh -r? / -t?

if [[ $1 == "-r" ]]; then
    $client_start
elif [[ $1 == "-t" ]]; then
    client_start="${client_start} -t"

    # run the commnad & return the process id
    $client_start &
    PID=$!
    echo "$PID" >>"server-pid.txt"
fi
