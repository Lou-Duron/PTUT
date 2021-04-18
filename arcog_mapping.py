#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os 
import mysql.connector as mc
import argparse
from configurations import config

try:
    # try connection the database
    conn = mc.connect(host = 'localhost',
    database = 'ptut', 
    user = config.BD_USER, # BD_USER by default in directroy configurations 
    password= config.BD_PASSWORD) # BD_PASSEWORD by default in directory configurations

                
except mc.Error as err: # si la connexion échoue
    print(err)

else: # si le connexion réussie
    cursor = conn.cursor()
    
    #Eggnog mapper
    cursor.execute("SELECT S.id_uniprot, sequence FROM proteins_cog AS P, strain_proteins AS S WHERE P.id_uniprot = S.id_uniprot AND id_cog = 'NA' AND sequence IS NOT NULL;")
    results = cursor.fetchall()
    
    eggnog_mapper_file = open("results/eggnog_mapper_file.fa", "w")
    for rows in results:
        eggnog_mapper_file.write(">"+rows[0]+"\n"+rows[1]+"\n")
    eggnog_mapper_file.close()
    cmd = (f"eggnog-mapper/./emapper.py --cpu 4 -i results/eggnog_mapper_file.fa --output arcogs_results.fa --output_dir results/ -m diamond -d none --tax_scope 2157 --go_evidence non-electronic --target_orthologs all --seed_ortholog_evalue 0.001 --seed_ortholog_score 60 --query_cover 20 --subject_cover 0 --override --temp_dir results/temp --block_size 1")
    os.system(cmd)

finally:
    conn.commit()
    if(conn.is_connected()):
        cursor.close() # close cursor
        conn.close() # close connection