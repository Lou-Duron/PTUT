#!/bin/bash

if [! command -v conda &> /dev/null]; then
    echo "COMMAND could not be found"
    exit
else
    echo "Please enter the name of the environnment you want to create"
    read -p 'Please Enter the name of your env ' nameEnv
    echo "Creating your conda env " $nameEnv
    conda create --name $nameEnv --file installation/spec-list.txt
fi
exit