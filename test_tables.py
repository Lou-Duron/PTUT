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
    conn = mc.connect(host='localhost',
                      database='ptut',
                      user=config.BD_USER,  # BD_USER by default in directroy configurations
                      password=config.BD_PASSWORD)  # BD_PASSEWORD by default in directory configurations


except mc.Error as err:  # si la connexion échoue
    print(err)

else:  # si le connexion réussie

    cursor = conn.cursor()  # Création du curseur

    # Test proteins number in the helicase file
    with open(args.helicasefile, "r") as fh:
        proteins_table_count = 0
        for line in fh:
            proteins_table_count += 1
        print("Number of proteins in the helicase file : ", proteins_table_count)

    # Test proteins number in the database that have an associated cog
    cursor.execute("SELECT DISTINCT id_uniprot FROM proteins_cog  WHERE id_cog != 'NA'")
    proteins_cog_table = cursor.fetchall()
    print("Number of proteins in the database that have an associated cog : ", len(proteins_cog_table))

    # Test proteins number in the database that doesn't have an associated cog
    cursor.execute("SELECT  id_uniprot FROM proteins_cog WHERE id_cog = 'NA'")
    proteins_NA_table = cursor.fetchall()
    print("Number of proteins in the database that doesn't have an associated cog : ", len(proteins_NA_table))

    # Test if there's the same amount of proteins in the database and in the helicase file
    print("same amount of proteins in database and file ?", proteins_table_count == len(proteins_NA_table) + len(proteins_cog_table))

    # Same number but some proteins can be in double ( Distinct in the previous request )

    print("\nMultiple Status ")

    # Test number of proteins that have a single status
    cursor.execute("SELECT COUNT(id_uniprot) FROM multiple_status WHERE multiple = 1")
    result_single_status = cursor.fetchall()
    print("Number of proteins with single status : ", result_single_status[0][0])

    # Test number of proteins that have a multiple status
    cursor.execute("SELECT COUNT(id_uniprot) FROM multiple_status WHERE multiple > 1")
    result_multiple_status = cursor.fetchall()
    print("Number of proteins with multiple status : ", result_multiple_status[0][0])

    # Test which proteins have a multiple status
    cursor.execute("SELECT id_uniprot, multiple FROM multiple_status WHERE multiple > 1")
    result = cursor.fetchall()
    print(result)

    print("\nAnnotations file")

    # Test number of arcogs in the annotation file
    with open(args.arcogs, "r") as fh:
        arcogs_table_count = 0
        for line in fh:
            arcogs_table_count += 1
        print("Number of arcogs in the annotation file : ", arcogs_table_count)

    # Test number of arcogs in the database
    cursor.execute("SELECT id_cog FROM cog")
    arcogs_table = cursor.fetchall()
    print("Number of arcogs in the table cog : ", len(arcogs_table))

    # Test if there's the same amount of arcogs in the database and in the annotation file
    print("Same amount of arcogs in file and database ?", arcogs_table_count == len(arcogs_table))

    # Same amount of arcogs + no doubles.



    # Reste à tester les obsoletes. -> combien et savoir si font parti des multiple ? ou de celles qu'on a pas d'arcog.
    # Tester parmi toutes les obsoletes est-ce qu'elles font parti de la requete multiple status ou de la requete pas d'arcog associé

    with open("results/obsolete_proteins", "r") as fh:
        for protein in fh:
            query =
            cursor.execute("SELECT multiple FROM multiple_status WHERE id_uniprot = (%s)", (protein,))
            print(cursor.fetchall())



query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query, (hire_start, hire_end))

for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))

cursor.close()
cnx.close()









finally:
    conn.commit()
    if(conn.is_connected()):
        cursor.close() # close cursor
        conn.close() # close connection



