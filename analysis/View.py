#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import argparse

################################################################################################
parser = argparse.ArgumentParser(description='View') 
parser.add_argument('--database', '-b', type = str, help = "database to connect to")
parser.add_argument('--host', '-o', type=str, required=False, help="type of database host, localhost by default")
parser.add_argument('--name', '-n', type = str, help = "name of the view")
parser.add_argument('--first', '-f', type = str, help = "name of the first table")
parser.add_argument('--second', '-s', type = str, help = "name of the second table")
parser.add_argument('--protein_nb', '-p', type=int, required=False, help="minimal number of protein for a given arcog")
parser.add_argument('--p_value', '-v', type=float, required=False, help="minimal p_value of mapped arcgos")
args = parser.parse_args()
###############################################################################################

try:
    conn = mc.connect(host=args.host,
    user=config.BD_USER,
    password=config.BD_PASSWORD) 

except mc.Error as err:
    print(err)

else:  
    cursor = conn.cursor()
    cursor.execute(f"USE {args.database}")
    cursor.execute(f"DROP VIEW IF EXISTS {args.name}")
    request = f"CREATE VIEW {args.name} AS SELECT f.id_uniprot, f.id_cog FROM {args.first} f LEFT JOIN {args.second} s ON f.id_uniprot = s.id_uniprot " 
    if args.protein_nb != None :
        request += f"WHERE f.id_cog IN (SELECT id_cog FROM paralogy WHERE proteins_count > {str(args.protein_nb)})" 
    request += f"UNION SELECT s.id_uniprot, s.id_cog FROM {args.first} f RIGHT JOIN {args.second} s ON f.id_uniprot = s.id_uniprot "
    if args.protein_nb != None :
        request += f"WHERE s.id_cog IN (SELECT id_cog FROM paralogy WHERE proteins_count > {str(args.protein_nb)})"
    cursor.execute(request)

