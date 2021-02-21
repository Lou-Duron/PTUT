#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
" My Sql conenctor library may require configuration of environment to solve Library dependencies. In this project a conda environment was used with the following commands
conda create -n project name
conda install -c anaconda mysql-connector-python
"

# Insertion for table x linking proteins classed in multiple orthologs groups
try:
    conn = mc.connector(host = '', database = '', user = '', password='')
    cursor = conn.cursor()
    
    request = "INSERT INTO table_x SELECT id_uniprot, count(id_uniprot) as multiple FROM table_1 GROUP BY id_uniprot"
    cursor.execute(req)

# Count of proteins and species for each ortholgs group (cogs) 
"""
Need of a table linking species to Id_prot 
"""
