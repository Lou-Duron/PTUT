#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import csv
import argparse
from configurations import config
import requests
from requests.exceptions import HTTPError

################################################################################################
parser = argparse.ArgumentParser(description='Database Creation') 
parser.add_argument('--helicasefile', '-f', type=str,
                    help="tsv file with CGBD id associated to uniprot protein id ")
parser.add_argument('--arcogs', '-c', type = str, required = False, help = "tsv file with id_cogs descriptions and type from eggnog" )

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
        cursor.execute("DROP TABLE IF EXISTS `proteins_cog`")
        cursor.execute("DROP TABLE IF EXISTS `cog`")
        cursor.execute("DROP VIEW IF EXISTS `multiple_status`")
        cursor.execute("DROP TABLE IF EXISTS `strain_proteins`")
        cursor.execute("DROP VIEW IF EXISTS `paralogy`")

    # Create tables if not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS `proteins_cog`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),PRIMARY KEY(`id_uniprot`, `id_cog`));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `cog`(`id_cog` VARCHAR(30) UNIQUE, `category` VARCHAR(100), `description` BLOB, PRIMARY KEY(`id_cog`));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `strain_proteins`(`strain` VARCHAR(30), `id_uniprot` VARCHAR(30), `sequence` BLOB, PRIMARY KEY(`id_uniprot`));")

    with open(args.helicasefile, "r") as fh:  # reading tsv entry file using args module
        tsv_helicases = csv.reader(fh, delimiter="\t")
        obsolete = []
        
        for line in tsv_helicases: #File with uniprot id and CBI id
            id_uniprot = line[1]            
            try:
                # Arcogs retrieval 
                arcogs = []    
                url_arcog = "https://www.uniprot.org/uniprot/"+id_uniprot+".txt" 
                arcog_response = requests.get(url_arcog)
                arcog_response.raise_for_status()  # If the response was successful, no Exception will be raised
                Embl_file = arcog_response.text.split("\n")
                
                if arcog_response.text == "":
                    obsolete.append(id_uniprot)
               
                for line_arc in Embl_file: #file 
                    if line_arc.startswith("DR   eggNOG"):
                        arcog = line_arc.split("; ")
                        arcogs.append(arcog[1])
                if arcogs: 
                    for el in arcogs:
                        cursor.execute("INSERT INTO proteins_cog (id_uniprot, id_cog) VALUES (%s,%s)", (id_uniprot, el)) #Insertion for proteins with cog
                else: 
                    cursor.execute("INSERT INTO proteins_cog (id_uniprot, id_cog) VALUES (%s,%s)", (id_uniprot, 'NA')) #Instertion for proteins with no cog
                    #Since NULL is not authorized as primary key, string 'NA' is used

                #sequence retrieval
                     # Strain retrieval 
                strain = line[0].split(".")
                strain = strain[0][0:5]
                url_seq = "https://www.uniprot.org/uniprot/"+id_uniprot+".fasta" 
                seq_response = requests.get(url_seq)
                seq_response.raise_for_status()  # If the response was successful, no Exception will be raised
                fasta = seq_response.text
                if fasta != '':
                    fasta = fasta.split("\n", 1)
                    seq = fasta[1].replace("\n",'')
                    cursor.execute("INSERT INTO strain_proteins (strain, id_uniprot, sequence) VALUES (%s,%s,%s)", (strain, id_uniprot,seq)) # Table with strain and proteins and sequence
                else:
                    cursor.execute("INSERT INTO strain_proteins (strain, id_uniprot, sequence) VALUES (%s,%s,%s)", (strain, id_uniprot, None)) # Table with strain and proteins and sequence

            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6

    
    with open(args.arcogs, "r") as fa: #Reading of cog description
        tsv_arcogs = csv.reader(fa, delimiter="\t")
        for line in tsv_arcogs:
            if line[3] == "":
                cursor.execute("INSERT INTO cog (id_cog, description, category) VALUES (%s,%s ,%s)", (line[1], None, line[2],))
            else: 
                cursor.execute("INSERT INTO cog (id_cog, description, category) VALUES (%s,%s ,%s)", (line[1], line[3], line[2]))
    
    #Views
    cursor.execute("CREATE VIEW multiple_status AS SELECT id_uniprot, count(*) AS multiple FROM proteins_cog GROUP BY id_uniprot;") #Proteins with multiple cogs associated
    cursor.execute("CREATE VIEW paralogy AS SELECT id_cog, count(strain) AS strain_count, count(id_uniprot) as proteins_count FROM proteins_cog NATURAL JOIN strain_proteins GROUP BY id_cog;") #strain and protein cog by cog

    obsolete_file = open("results/obsolete_proteins", "w")
    for proteins in obsolete:
        obsolete_file.write(proteins + "\n")
    obsolete_file.close()

finally:
    conn.commit()
    if(conn.is_connected()):
        cursor.close() # close cursor
        conn.close() # close connection