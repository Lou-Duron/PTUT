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

 # https://docs.fedoraproject.org/en-US/quick-docs/installing-mysql-mariadb/
sudo dnf install https://repo.mysql.com//mysql80-community-release-fc31-1.noarch.rpm
sudo dnf install mysql-community-server
sudo systemctl start mysqld
sudo systemctl enable mysqld
sudo mysql_secure_installation

mkdir results
mkdir data
wget data/ http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_annotations.tsv.gz
gunzip data/2157_annotations.tsv.gz

mkdir configurations
printf "${green}Need to enter username and password of mysql"
printf "${green}Please enter your username\n${reset}" 
read -i -e username
printf "${green}Please enter your password\n${reset}"
read -s password
printf "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nBD_USER = $username\nBD_PASSWORD = $password\n" > configurations/test.txt
printf "${green}if you need to change the user/password, follow this path${reset}\n"
printf "configurations/config.py${reset}\n" 
printf "- end of installation -\n"
exit

exit
