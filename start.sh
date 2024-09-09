#!/bin/bash
# script to start the system in one of the two modes

mode=$1
num_pubs=$2
num_subs=$3
re='^[0-9]+$'

if [[ $mode != "rabbitmq" ]] && [[ $mode != "zeromq" ]]
then
    echo "Usage: <rabbitmq|zeromq> <num_pubs> <num_subs>"
    exit 1
fi

if !([[ $num_pubs =~ $re ]] && [[ $num_subs =~ $re ]])
then
    echo "Usage: <rabbitmq|zeromq> <num_pubs> <num_subs>"
    exit 1
fi

cd $mode
python3 main.py $num_pubs $num_subs
