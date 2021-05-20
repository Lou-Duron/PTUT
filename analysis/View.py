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
parser.add_argument('--first_suffix', '-f', type = str, help = "name of the first suffix table")
parser.add_argument('--second_suffix', '-s', type = str, help = "name of the second suffix table")
parser.add_argument('--protein_nb', '-p', type=int, required=False, help="minimal number of protein for a given arcog")
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
    request = (f"CREATE VIEW {args.name} AS "
        "SELECT f.id_uniprot, f.id_cog "
        f"FROM proteins_cog_{args.first_suffix} f "
        f"LEFT JOIN proteins_cog_{args.second_suffix} s ON f.id_uniprot = s.id_uniprot "
        "WHERE f.id_uniprot NOT IN "
        "(SELECT id_uniprot "
        f"FROM proteins_cog_{args.first_suffix} "
        "WHERE id_cog = 'NA' "
        "AND id_uniprot IN( "
        "SELECT id_uniprot "
        f"FROM proteins_cog_{args.second_suffix} "
        "WHERE id_cog != 'NA')) ") 
    if args.protein_nb is not None :
        request += (f"AND f.id_cog IN ("
            f"SELECT id_cog FROM paralogy_{args.first_suffix} "
            f"WHERE proteins_count > {str(args.protein_nb)})") 
    request += (f"UNION SELECT s.id_uniprot, s.id_cog "
        f"FROM proteins_cog_{args.first_suffix} f "
        f"RIGHT JOIN proteins_cog_{args.second_suffix} s ON f.id_uniprot = s.id_uniprot "
        "WHERE s.id_uniprot NOT IN "
        "(SELECT id_uniprot "
        f"FROM proteins_cog_{args.second_suffix} "
        "WHERE id_cog = 'NA' "
        "AND id_uniprot IN( "
        "SELECT id_uniprot "
        f"FROM proteins_cog_{args.first_suffix} "
        "WHERE id_cog != 'NA')) ") 
    if args.protein_nb is not None :
        request += (f"AND s.id_cog IN ("
            f"SELECT id_cog FROM paralogy_{args.second_suffix} "
            f"WHERE proteins_count > {str(args. protein_nb)})")
    cursor.execute(request)
    
    

    # Infos
    cursor.execute(f"SELECT id_uniprot, id_cog FROM {args.name}")
    id_uniprot = []
    id_cog = []
    rows = 0
    for el in cursor:
        rows += 1
        if el[0] not in id_uniprot:
            id_uniprot.append(el[0])
        if el[1] not in id_cog:
            if el[1] != 'NA':
                id_cog.append(el[1])
    print(f"Done :\n{rows} rows in set\n{len(id_uniprot)} proteins\n{len(id_cog)} distinct arcogs")



