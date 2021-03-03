#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
"""
My Sql conenctor library may require configuration of environment to solve Library dependencies.
see ReadMe
"""

# Insertion for table x linking proteins classed in multiple orthologs groups
try:
    conn = mc.connector(host = '', database = '', user = '', password='')
    cursor = conn.cursor()
    
    request = "INSERT INTO table_x SELECT id_uniprot, count(id_uniprot) as multiple FROM table_1 GROUP BY id_uniprot"
    cursor.execute(req)

# Count of proteins and species for each ortholgs group (cogs) 
#Need of a table linking species to Id_prot 

from configurations import config
""" 
My Sql conenctor library may require configuration of environment to solve Library dependencies.
see ReadMe
"""
mydb = mc.connect(
  host="localhost",
  user=config.BD_USER,
  password=config.BD_PASSWORD
)
