#!/bin/bash
source "./script/linux/config.sh"

server_start="${pythonalias} server/app.py"

# this-file.sh -t? <password>?

if [[ $1 == "-r" ]]
then

    if [[ $2 != "" ]]
    then
        server_start="${server_start} -p=$2"
    fi

    $server_start
fi
