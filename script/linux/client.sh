#!/bin/bash
source "./script/linux/config.sh"

client_start="${pythonalias} client/app.py"
# this-file.sh -r? <INP_FILE_PATH>? <OUT_FILE_PATH>?

if [[ $1 == "-r" ]]
then
    if [[ $2 != "" ]]
    then
        client_start="${client_start} -t --inpf=\"$2\" --outf=\"$3\""
    fi

    $client_start
fi
