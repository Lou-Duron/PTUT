#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import csv
import argparse
from configurations import config
import urllib.parse
import urllib.request

################################################################################################
parser = argparse.ArgumentParser(description='') 
parser.add_argument('--helicasefile', '-f', dest="heli_file", type=str,
                    help="tsv file containing CGBD id and associated helicase designated by its uniprot protein id")
parser.add_argument('--drop', '-d', required=False, action="store_true", help='If needed to drop the tables first')
'''
parser.add_argument('--membersfile', '-m', dest="members_file", type=str,
                    help="tsv file containing -> to complete (see readme from eggnog)")
'''

args = parser.parse_args()
###############################################################################################


try:
    # Connection à la base de donnée
    conn = mc.connect(host = 'localhost',
    database = 'ptut', 
    user = config.BD_USER, # nom user dans le fichier config
    password= config.BD_PASSWORD) # mot de passe dans le fichier config
                
except mc.Error as err: # si la connexion échoue
    print(err)

else: # si le connexion réussie

    cursor = conn.cursor() # Création du curseur

    # Drop tables if new changes
    if args.drop :
        cursor.execute("DROP TABLE `PROTEINS_COG`")
        cursor.execute("DROP TABLE `COG`")
        cursor.execute("DROP TABLE `MULTIPLE_STATUS`")

    # Create tables if not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS `PROTEINS_COG`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),PRIMARY KEY(`id_uniprot`, `id_cog`));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `COG`(`id_cog` VARCHAR(30) UNIQUE, `description` VARCHAR(100), `category` VARCHAR(30), `species_count` VARCHAR(10), `proteins_count` VARCHAR(10),PRIMARY KEY(`id_cog`));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `MULTIPLE_STATUS`(`client_id` VARCHAR(30), `id_uniprot`VARCHAR(30), `multiple`VARCHAR(30), `predicted_by`VARCHAR(30), PRIMARY KEY(`client_id`));")

    with open(args.heli_file, "r") as fh:  # reading tsv entry file using args module
        # helifile ?
        tsv = csv.reader(fh, delimiter="\t")
       



finally: # s'execute de toute facon
    conn.commit() # commit changes
    if(conn.is_connected()):
        cursor.close() # ferme le cursor
        conn.close() # ferme la connexion
