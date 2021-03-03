#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import csv
from configuration import config


try:
    conn = mc.connect(host = 'localhost',
    database = 'ptut', 
    user = config.BD_USER, 
    password= config.BD_PASSWORD)
    
    cursor = conn.cursor()

    cursor.execute("DROP TABLE `PROTEINS_COG`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `PROTEINS_COG`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),PRIMARY KEY(`id_uniprot`, `id_cog`));")

    #cursor.execute("DROP TABLE `COG`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `COG`(`id_cog` VARCHAR(30) UNIQUE, `description` VARCHAR(100), `category` VARCHAR(30), `species_count` VARCHAR(10), `proteins_count` VARCHAR(10),PRIMARY KEY(`id_cog`));")

    #cursor.execute("DROP TABLE `MULTIPLE_STATUS`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `MULTIPLE_STATUS`(`client_id` VARCHAR(30), `id_uniprot`VARCHAR(30), `multiple`VARCHAR(30), `predicted_by`VARCHAR(30), PRIMARY KEY(`client_id`));")


    
    with open("/home/lou/Master/PTUT/ptut_helicases/data/uniprot_eggnog.Nov2018.tsv", "r") as fh: # a mettre en argument 
        tsv = csv.reader(fh, delimiter="\t")
        for ligne in tsv:
            cog_id = ligne[1].split(",")
            print(cog_id)
            for id in len(cog_id):
                cursor.execute("INSERT INTO PROTEINS_COG (id_uniprot, id_cog) VALUES (%s,%s)", (ligne[0], id))

            
    conn.commit()


except mc.Error as err: # si la connexion échoue
    print(err)

finally: # s'execute de toute facon
    if(conn.is_connected()):
        cursor.close() # ferme le cursor
        conn.close() # ferme la connexion
