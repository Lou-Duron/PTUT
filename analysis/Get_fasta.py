#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os 
import mysql.connector as mc
import argparse
from pathlib import Path
from configurations import config

################################################################################################
parser = argparse.ArgumentParser(description='Fasta File for eggnog mapper search')
parser.add_argument('--database', '-b', type = str, help = "database to connect to")
parser.add_argument('--name', '-n', type=str, required=False, default='seqtosearch', help='filename')
parser.add_argument('--all', '-a', required=False, action="store_true", help='get all proteins')
parser.add_argument('--partial', '-p',required=False, action="store_true", help='get only proteins without arcogs')
args = parser.parse_args()
###############################################################################################

rootpath = Path(__file__).resolve().parent.parent #Get root path of project

try:
    # try connection the database
    conn = mc.connect(host = 'localhost',
    database = args.database, 
    user = config.BD_USER, # BD_USER by default in directroy configurations 
    password= config.BD_PASSWORD) # BD_PASSEWORD by default in directory configurations

                
except mc.Error as err: # if connection failed
    print(err)

else: # if connection succeed
    cursor = conn.cursor()
    
    if args.partial:
        cursor.execute("SELECT DISTINCT(S.id_uniprot), sequence FROM proteins_cog AS P, strain_proteins AS S WHERE P.id_uniprot = S.id_uniprot AND id_cog = 'NA' AND sequence IS NOT NULL;")
        results = cursor.fetchall() 
    
    if args.all:
        cursor.execute("SELECT DISTINCT(S.id_uniprot), sequence FROM proteins_cog AS P, strain_proteins AS S WHERE P.id_uniprot = S.id_uniprot AND sequence IS NOT NULL;")
        results = cursor.fetchall() 

    filepath = rootpath / f"analysis/results/{args.name}.fa"
    eggnog_mapper_file = open(filepath, "w")
    for rows in results:
        eggnog_mapper_file.write(">"+rows[0]+"\n"+rows[1]+"\n")
    eggnog_mapper_file.close()
    

    conn.commit()
    cursor.close() # close cursor
    conn.close() # close connection
