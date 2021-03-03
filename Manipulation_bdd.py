#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import csv
from configurations import config
try:
    conn = mc.connect(host = 'localhost',
    database = 'ptut', 
    user = 'root', 
    password=config.BD_PASSWORD)
    
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS `PROTEINS_COG`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),PRIMARY KEY(`id_uniprot`, `id_cog`));")

    cursor.execute("CREATE TABLE IF NOT EXISTS `COG`(`id_cog` VARCHAR(30) UNIQUE, `description` VARCHAR(100), `category` VARCHAR(30), `species_count` VARCHAR(10), `proteins_count` VARCHAR(10),PRIMARY KEY(`id_cog`));")

    cursor.execute("CREATE TABLE IF NOT EXISTS `MULTIPLE_STATUS`(`client_id` VARCHAR(30), `id_uniprot`VARCHAR(30), `multiple`VARCHAR(30), `predicted_by`VARCHAR(30), PRIMARY KEY(`client_id`));")

    with open("uniprot_eggnog.Nov2018.tsv", "r") as fh:  
        tsv = csv.reader(fh, delimiter="\t")
        for ligne in tsv:
            if len(ligne[1]) < 100:
                cursor.execute("INSERT INTO PROTEINS_COG (id_uniprot, id_cog) VALUES (%s,%s)", (ligne[0], ligne[1]))

            
    conn.commit()

except mc.Error as err: # si la connexion échoue
    print(err)

finally: # s'execute de toute facon
    if(conn.is_connected()):
        cursor.close() # ferme le cursor
        conn.close() # ferme la connexion
