#!/bin/bash

source "./script/linux/config.sh"
source "./script/linux/server.sh"
source "./script/linux/client.sh"

bash ./script/linux/server.sh -r 123 &
bash ./script/linux/client.sh -r &

$pythonalias -m pytest test/

# TODO: shutdown the apps