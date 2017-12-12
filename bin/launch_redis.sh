#!/bin/bash

set -e
set -x

[ -z "$AIL_HOME" ] && echo "Needs the env var AIL_HOME. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_REDIS" ] && echo "Needs the env var AIL_REDIS. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_LEVELDB" ] && echo "Needs the env var AIL_LEVELDB. Run the script from the virtual environment." && exit 1;

conf_dir="${AIL_HOME}/configs/"

screen -dmS "Redis_AIL"
sleep 0.1
echo -e $GREEN"\t* Launching Redis servers"$DEFAULT
screen -S "Redis_AIL" -X screen -t "6379" bash -c 'redis-server '$conf_dir'6379.conf ; read x'
sleep 0.1
screen -S "Redis_AIL" -X screen -t "6380" bash -c 'redis-server '$conf_dir'6380.conf ; read x'
sleep 0.1
screen -S "Redis_AIL" -X screen -t "6381" bash -c 'redis-server '$conf_dir'6381.conf ; read x'

# For Words and curves
sleep 0.1
# escaping / for sed
preProcessedPath=$(echo $AIL_HOME | sed 's_/_\\/_g')
# Replacing variable in 6382.conf by the path and writting the modified config into a temp file
sed 's/{AIL_HOME}/'$preProcessedPath'/g' < $conf_dir'6382.conf' > $conf_dir'temp6382.conf'
screen -S "Redis_AIL" -X screen -t "6382" bash -c 'redis-server '$conf_dir'temp6382.conf ; read x'
