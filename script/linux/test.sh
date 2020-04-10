#!/bin/bash

source "./script/linux/config.sh"
source "./script/linux/server.sh"
source "./script/linux/client.sh"

redis-server redis.conf &

bash ./script/linux/server.sh -r 123 &
bash ./script/linux/client.sh -r -t &

$pythonalias -m pytest test/

sleep 1s

SERVER_PID=$(cat "server-pid.txt")
CLIENT_PID=$(cat "client-pid.txt")

kill -9 $SERVER_PID
kill -9 $CLIENT_PID

rm "server-pid.txt"
rm "client-pid.txt"