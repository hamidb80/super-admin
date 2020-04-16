#!/bin/bash

source "./script/linux/config.sh"
source "./script/linux/server.sh"
source "./script/linux/client.sh"

export server_pass="123"

# init message queue server
redis-server redis.conf &

bash ./script/linux/server.sh -t "$server_pass" &
bash ./script/linux/client.sh -t &

sleep 1s

SERVER_PID=$(cat "server-pid.txt")
CLIENT_PID=$(cat "client-pid.txt")

$pythonalias -m pytest test/

kill -9 $SERVER_PID
kill -9 $CLIENT_PID

rm "server-pid.txt"
rm "client-pid.txt"
