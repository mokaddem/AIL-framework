#!/bin/bash

set -e
set -x

[ -z "$AIL_HOME" ] && echo "Needs the env var AIL_HOME. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_REDIS" ] && echo "Needs the env var AIL_REDIS. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_LEVELDB" ] && echo "Needs the env var AIL_LEVELDB. Run the script from the virtual environment." && exit 1;

screen -dmS "Queue_AIL"
sleep 0.1

echo -e $GREEN"\t* Launching all the queues"$DEFAULT
screen -S "Queue_AIL" -X screen -t "Queues" bash -c $AIL_BIN'launch_queues.py; read x'
