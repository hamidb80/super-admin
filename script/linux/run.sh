#!/bin/bash

source "./script/linux/config.sh"

source "./script/linux/server.sh"
source "./script/linux/client.sh"

# open server
gnome-terminal -e "$server_start"
# open client
gnome-terminal -e "$client_start"
