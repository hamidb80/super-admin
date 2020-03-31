#!/bin/bash

source "./script/linux/config.sh"
source "./script/linux/server.sh"
source "./script/linux/client.sh"

INP_FILE_PATH="$(pwd)/inp.txt"
OUT_FILE_PATH="$(pwd)/out.txt"

bash "$(pwd)/script/linux/server.sh -r 123"
bash "$(pwd)/script/linux/client.sh -r \"${INP_FILE_PATH}\" \"${OUT_FILE_PATH}\""

$pythonalias -m pytest test/