#!/bin/bash

set -e
set -x

[ -z "$AIL_HOME" ] && echo "Needs the env var AIL_HOME. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_REDIS" ] && echo "Needs the env var AIL_REDIS. Run the script from the virtual environment." && exit 1;
[ -z "$AIL_LEVELDB" ] && echo "Needs the env var AIL_LEVELDB. Run the script from the virtual environment." && exit 1;

echo -e "\t* Checking configuration"
bash -c $AIL_BIN"Update-conf.py"
exitStatus=$?
if [ $exitStatus -ge 1 ]; then
    echo -e $RED"\t* Configuration not up-to-date"$DEFAULT
    exit
fi
echo -e $GREEN"\t* Configuration up-to-date"$DEFAULT

screen -dmS "Script_AIL"
sleep 0.1
echo -e $GREEN"\t* Launching ZMQ scripts"$DEFAULT

screen -S "Script_AIL" -X screen -t "ModuleInformation" bash -c $AIL_BIN'ModulesInformationV2.py -k 0 -c 1; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Mixer" bash -c $AIL_BIN'Mixer.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Global" bash -c $AIL_BIN'Global.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Duplicates" bash -c $AIL_BIN'Duplicates.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Attributes" bash -c $AIL_BIN'Attributes.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Lines" bash -c $AIL_BIN'Lines.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "DomClassifier" bash -c $AIL_BIN'DomClassifier.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Categ" bash -c $AIL_BIN'Categ.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Tokenize" bash -c $AIL_BIN'Tokenize.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "CreditCards" bash -c $AIL_BIN'CreditCards.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Onion" bash -c $AIL_BIN'Onion.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Mail" bash -c $AIL_BIN'Mail.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Web" bash -c $AIL_BIN'Web.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Credential" bash -c $AIL_BIN'Credential.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Curve" bash -c $AIL_BIN'Curve.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "CurveManageTopSets" bash -c $AIL_BIN'CurveManageTopSets.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "RegexForTermsFrequency" bash -c $AIL_BIN'RegexForTermsFrequency.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "SetForTermsFrequency" bash -c $AIL_BIN'SetForTermsFrequency.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Indexer" bash -c $AIL_BIN'Indexer.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Keys" bash -c $AIL_BIN'Keys.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Phone" bash -c $AIL_BIN'Phone.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Release" bash -c $AIL_BIN'Release.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "Cve" bash -c $AIL_BIN'Cve.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "WebStats" bash -c $AIL_BIN'WebStats.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "ModuleStats" bash -c $AIL_BIN'ModuleStats.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "SQLInjectionDetection" bash -c $AIL_BIN'SQLInjectionDetection.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "alertHandler" bash -c $AIL_BIN'alertHandler.py; read x'
sleep 0.1
screen -S "Script_AIL" -X screen -t "SentimentAnalysis" bash -c $AIL_BIN'SentimentAnalysis.py; read x'


