#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import argparse
from pathlib import Path
from configurations import config
import csv
import re

rootpath = Path(__file__).resolve().parent.parent #Get root path of project

################################################################################################
parser = argparse.ArgumentParser(description='Verification of database creation')
parser.add_argument('--host', '-o', type=str, help="host connection")
parser.add_argument('--database', '-b', type=str, required=True, help="database to connect to")
parser.add_argument('--helicasefile', '-f', type=str, required=False,
                    help="tsv file with CGBD id associated to uniprot protein id ")
parser.add_argument('--mapper', '-m', type=str, required=False, help="annotation file from the eggnog mapper")
parser.add_argument('--cogs', '-c', type=str, required=True, help = "tsv file with id_cogs descriptions and type")
parser.add_argument('--suffix', '-s',  type=str, required=True, help="the table you want to test")
parser.add_argument('--multiple', '-u', type=str, required=False, default='multiple_status', help='filename for multiple status proteins')
parser.add_argument('--name', '-n', type=str, required=False, default='obsolete',
                    help='filename of obsolete uniprot id (default obsolete.txt)')
args = parser.parse_args()
###############################################################################################

"""
Test database creation and show results
Run this after running the ....
"""

try:
    # try connection the database
    conn = mc.connect(host=args.host,
                      database=args.database,
                      user=config.BD_USER,  # BD_USER by default in directroy configurations
                      password=config.BD_PASSWORD)  # BD_PASSEWORD by default in directory configurations


except mc.Error as err:  # if connexion fails
    print(err)

else:  # if connexion is open

    cursor = conn.cursor()  # Création du curseur

    # Test proteins number in the helicase file
    if args.helicasefile:
        with open(args.helicasefile, "r") as fh:
            proteins_file_count = 0
            for line in fh:
                proteins_file_count += 1
            print("Number of proteins in the helicase file : ", proteins_file_count)

        with open(args.name, "r") as fh:
            obsolete_proteins_count = 0
            for protein in fh:
                obsolete_proteins_count += 1

        print("Number of obsolete proteins : ", obsolete_proteins_count)

        # Test proteins number in the database that have an associated cog
        cursor.execute(f"SELECT DISTINCT id_uniprot FROM proteins_cog_{args.suffix}  WHERE id_cog != 'NA';")
        proteins_cog_table = cursor.fetchall()
        print("Number of proteins in the database that have been associated to one or multiple COG : ",
              len(proteins_cog_table))

        # Test proteins number in the database that doesn't have an associated cog
        cursor.execute(f"SELECT id_uniprot FROM proteins_cog_{args.suffix} WHERE id_cog = 'NA';")
        proteins_NA_table = cursor.fetchall()
        print("Number of proteins in the database that doesn't have an associated cog : ", len(proteins_NA_table))
         # Test if there's the same amount of proteins in the database and in the helicase file
        print("Number of proteins in database equals to proteins in file minus the obsolete?", proteins_file_count - obsolete_proteins_count  == len(proteins_NA_table) + len(proteins_cog_table))

        print("Note : obsolete id_uniprot are not inserted into the database and are written in the following file results/obsolete_proteins.txt")


    if args.mapper:
        with open(args.mapper, "r") as fh:
            proteins_file_count = 0
            tsv_emapper = csv.reader(fh, delimiter="\t")
            motif = re.compile(r"(arC.*@2157)")
            for line in tsv_emapper:
                if re.search("^[A-Z]", line[0]):
                    proteins_file_count += 1

        # Test proteins number in the database that have an associated cog
        cursor.execute(f"SELECT DISTINCT id_uniprot FROM proteins_cog_{args.suffix}  WHERE id_cog != 'NA';")
        proteins_cog_table = cursor.fetchall()
        print("Number of proteins in the database that have been associated to one or multiple COG : ",
              len(proteins_cog_table))

        # Test proteins number in the database that doesn't have an associated cog
        cursor.execute(f"SELECT id_uniprot FROM proteins_cog_{args.suffix} WHERE id_cog = 'NA';")
        proteins_NA_table = cursor.fetchall()
        print("Number of proteins in the database that doesn't have an associated cog : ", len(proteins_NA_table))

        # Test if there's the same amount of proteins in the database and in the helicase file
        print("Number of proteins in database equals to proteins in file",
              proteins_file_count == len(proteins_NA_table) + len(proteins_cog_table))

    # Same number but some proteins can be in double ( Distinct in the previous request )
    print("\nMultiple Status ")

    # Test number of proteins that have a single status
    cursor.execute(f"SELECT COUNT(id_uniprot) FROM multiple_status_{args.suffix} WHERE multiple = 1;")
    result_single_status = cursor.fetchall()
    print("Number of proteins with single status : ", result_single_status[0][0])

    # Test number of proteins that have a multiple status
    cursor.execute(f"SELECT COUNT(id_uniprot) FROM multiple_status_{args.suffix} WHERE multiple > 1;")
    result_multiple_status = cursor.fetchall()
    print("Number of proteins with multiple status : ", result_multiple_status[0][0])

    # Retrieve proteins with multiple status
    cursor.execute(f"SELECT id_uniprot FROM multiple_status_{args.suffix} WHERE multiple > 1;")
    results = cursor.fetchall()

    if args.multiple:
        multiplepath = rootpath / f"analysis/results/{args.multiple}.txt"
        multiple = open(multiplepath, "w")
        for proteins in results:
            multiple.write(proteins[0] + "\n")
        multiple.close()
        print(f"proteins with multiple status have been written in the following file results/{args.multiple}.txt")


    print("\nCogs")

    # Test number of cogs associated with our proteins that are type S
    cursor.execute(f"SELECT count(category) FROM cog WHERE category = 'S' AND id_cog IN (SELECT id_cog FROM proteins_cog_{args.suffix}"
                   f" WHERE id_cog != 'NA');")
    result_type_S = cursor.fetchall()
    print("Number of proteins which are associated with a type S COG : ", result_type_S[0][0])

    # Test number of unique COG in our database
    cursor.execute(f"SELECT COUNT(DISTINCT id_cog) FROM proteins_cog_{args.suffix};")
    reslut_unique_cog = cursor.fetchall()
    print("Number of unique cog associated to our proteins : ", reslut_unique_cog[0][0]-1)

    print("\nAnnotations file")

    # Test number of arcogs in the annotation file
    if args.cogs:
        with open(args.cogs, "r") as fh:
            arcogs_file_count = 0
            for line in fh:
                arcogs_file_count += 1
            print("Number of COGs in the annotation file : ", arcogs_file_count)

        # Test number of arcogs in the database
        cursor.execute(f"SELECT id_cog FROM cog")
        arcogs_table = cursor.fetchall()
        print("Number of COGs in the table cog : ", len(arcogs_table))

        # Test if there's the same amount of arcogs in the database and in the annotation file
        print("Number of COGs in database equals to COGs in file", arcogs_file_count == len(arcogs_table))

    cursor.close()
    conn.commit()
    if conn.is_connected():
        cursor.close()  # close cursor
        conn.close()  # close connection