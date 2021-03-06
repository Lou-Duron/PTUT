#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

SCRIPTPATH=`dirname $(realpath $0)` #get directory path of install.sh
ROOTPROJECT=$(builtin cd $SCRIPTPATH/..; pwd) #get path of the project root
echo $ROOTPROJECT

echo $DIRECTORY
if ! command -v conda &> /dev/null; then
    printf "${red}conda could not be found "
    printf "To install conda refers to https://conda.io/projects/conda/en/latest/user-guide/install/index.html${reset}\n"
    exit
else
	printf "${green}Please Enter the name of your environnment : ${reset}\n"
	read -i -e nameEnv
    echo "${green}Creating your conda env $nameEnv ${reset}" 
    conda env create --name $nameEnv --file $ROOTPROJECT/installation/environment.yml
fi

if ! command -v mysql &> /dev/null; then
    printf "${red}Mysql could not be found "
    printf "To install Mysql refers to https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/${reset}\n"
    exit
else
	pwd
    mkdir -p $ROOTPROJECT/data
    mkdir -p $ROOTPROJECT/analysis/configurations
    wget -O $ROOTPROJECT/data/2157_annotations.tsv.gz http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_annotations.tsv.gz
    gunzip $ROOTPROJECT/data/2157_annotations.tsv.gz
    printf "${green}Need to enter username and mysql password to connect to the desired database\n"
    printf "${red}NOTE: USER AND PASSWORD ARE NOT ENCRYPTED AND WILL BE STORED IN CLEAR TEXT${reset}\n"
    printf "${green}Please enter your username\n${reset}" 
    read -i -e username
    printf "${green}Please enter your password\n${reset}"
    read -s password
    printf "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nBD_USER = '$username'\nBD_PASSWORD = '$password'\n" > $ROOTPROJECT/analysis/configurations/config.py
    printf "${green}if you need to change the user/password, follow this path${reset}\n"
    printf "analysis/configurations/config.py${reset}\n" 
    printf "end of installation\n"
fi
exit



