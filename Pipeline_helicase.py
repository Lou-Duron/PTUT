#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import csv
import argparse
from configurations import config
import requests
from requests.exceptions import HTTPError

################################################################################################
parser = argparse.ArgumentParser(description='') 
parser.add_argument('--helicasefile', '-f', type=str,
                    help="tsv file with CGBD id associated to uniprot protein id ")
parser.add_argument('--arcogs', '-c', type = str, help = "tsv file with id_cogs descriptions and type from eggnog" )

parser.add_argument('--drop', '-d', required=False, action="store_true", help='drop all tables')

args = parser.parse_args()
###############################################################################################

try:
    # try connection the database
    conn = mc.connect(host = 'localhost',
    database = 'ptut', 
    user = config.BD_USER, # BD_USER by default in directroy configurations 
    password= config.BD_PASSWORD) # BD_PASSEWORD by default in directory configurations
                
except mc.Error as err: # si la connexion échoue
    print(err)

else: # si le connexion réussie

    cursor = conn.cursor() # Création du curseur

    # Drop tables if new changes
    if args.drop :
        cursor.execute("DROP TABLE `proteins_cog`")
        cursor.execute("DROP TABLE `cog`")
        cursor.execute("DROP VIEW `multiple_status`")

    # Create tables if not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS `proteins_cog`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),PRIMARY KEY(`id_uniprot`, `id_cog`));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `cog`(`id_cog` VARCHAR(30) UNIQUE, `category` VARCHAR(100), `description` BLOB, PRIMARY KEY(`id_cog`));")


    with open(args.helicasefile, "r") as fh:  # reading tsv entry file using args module
        tsv_helicases = csv.reader(fh, delimiter="\t")
        for line in tsv_helicases:
            print(line[1])
            arcogs = []
            try:
                url = "https://www.uniprot.org/uniprot/"+line[1]+".txt" 
                response = requests.get(url)
                # If the response was successful, no Exception will be raised
                response.raise_for_status()
                file = response.text.split("\n")
                for line_arc in file: 
                    if line_arc.startswith("DR   eggNOG"):
                        arcog = line_arc.split("; ")
                        arcogs.append(arcog[1])
                if arcogs:
                    for el in arcogs:
                        cursor.execute("INSERT INTO proteins_cog (id_uniprot, id_cog) VALUES (%s,%s)", (line[1], el))
                else: 
                    cursor.execute("INSERT INTO proteins_cog (id_uniprot, id_cog) VALUES (%s,%s)", (line[1], 'NA'))

                
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
        
        cursor.execute("CREATE VIEW multiple_status AS SELECT id_uniprot, count(*) FROM PROTEINS_COG GROUP BY id_uniprot;")
    
    with open(args.arcogs, "r") as fa:
        tsv_arcogs = csv.reader(fa, delimiter="\t")
        for line in tsv_arcogs:
            print(line[3])
            if line[3] == "":
                cursor.execute("INSERT INTO cog (id_cog, description, category) VALUES (%s,%s ,%s)", (line[1],'NA', line[2],))
            else: 
                cursor.execute("INSERT INTO cog (id_cog, description, category) VALUES (%s,%s ,%s)", (line[1], line[3], line[2]))

finally:
    conn.commit()
    if(conn.is_connected()):
        cursor.close() # close cursor
        conn.close() # close connection

    
          
