#!/bin/bash
source "./script/linux/config.sh"

server_start="${pythonalias} server/app.py"

# this-file.sh -r? -t? <password>?

if [[ $1 == "-r" ]]
then

    if [[ $3 != "" ]]
    then
        server_start="${server_start} -p=$2"
    fi

    if [[ $2 == "-t" ]]
    then
        # run the commnad & return the process id
        $server_start & PID=$!
        echo "$PID" >> "client-pid.txt"
    fi


    $server_start
fi
