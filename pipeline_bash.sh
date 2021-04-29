#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

if [! command -v conda &> /dev/null]; then
    printf "${red}conda could not be found "
    printf "To install conda refers to https://conda.io/projects/conda/en/latest/user-guide/install/index.html${reset}"
    exit
else
    echo "${green}Please enter the name of the environnment you want to create"
    read -p "${green}Please Enter the name of your environnment${reset} " nameEnv
    echo "${green}Creating your conda env $nameEnv ${reset}" 
    conda create --name $nameEnv --file installation/spec-list.txt
fi

if [! command -v mysql &> /dev/null]; then
    printf "${red}Mysql could not be found "
    printf "To install conda refers to https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/${reset}"
    exit
else
    mkdir results
    mkdir data
    mkdir configurations

    wget -O data/2157_annotations.tsv.gz http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_annotations.tsv.gz
    tar -xvzf data/2157_annotations.tsv.gz
    printf "${green}Need to enter username and password of mysql\n"
    printf "${green}Please enter your username\n${reset}" 
    read -i -e username
    printf "${green}Please enter your password\n${reset}"
    read -s password
    printf "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nBD_USER = $username\nBD_PASSWORD = $password\n" > configurations/config.txt
    printf "${green}if you need to change the user/password, follow this path${reset}\n"
    printf "configurations/config.py${reset}\n" 
    printf "end of installation\n"
fi
exit



