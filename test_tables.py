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
        print("There is' ", proteins_table_count, " proteins in the helicase file")

    # Test proteins number in the database that have an associated cog
    cursor.execute("SELECT DISTINCT id_uniprot FROM proteins_cog  WHERE id_cog != 'NA'")
    proteins_cog_table = cursor.fetchall()
    print("There'is ", len(proteins_cog_table), " proteins in the database that does have an associated  cog")

    # Test proteins number in the database that doesn't have an associated cog
    cursor.execute("SELECT  id_uniprot FROM proteins_cog WHERE id_cog = 'NA'")
    proteins_NA_table = cursor.fetchall()
    print("There'is ", len(proteins_NA_table), " proteins in the database that doesn't have an associated cog")

    # Test if there's the same amount of proteins in the database and in the helicase file
    print(proteins_table_count == len(proteins_NA_table) + len(proteins_cog_table))

    # Test if there's the same amount of proteins in the database and in the helicase file
    cursor.execute("SELECT id_cog FROM proteins_cog GROUP_BY id_cog WHERE id_cog = ( SELECT id_cog FROM cog GROUP_BY id_cog )")
    result = cursor.fetchall()
    print(result)
    print("There'is ", len(result), " proteins in the database that doesn't have an associated cog")

    """# Test if there is
    cursor.execute("SELECT COUNT (id_cog) FROM proteins_cog GROUP_BY id_cog WHERE id_cog = ( SELECT id_cog FROM cog GROUP_BY id_cog )")
    result = cursor.fetchall()
    print(result)"""

    # Test number of proteins that have a multiple status
    cursor.execute("SELECT COUNT (id_uniprot) FROM multiple_status WHERE multiple != 1")
    result = cursor.fetchall()
    print(result)

    # Test number of proteins that have a single status
    cursor.execute("SELECT COUNT (id_uniprot) FROM multiple_status WHERE multiple = 1")
    result = cursor.fetchall()
    print(result)



finally:
    conn.commit()
    if(conn.is_connected()):
        cursor.close() # close cursor
        conn.close() # close connection



