#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import argparse
from pathlib import Path

################################################################################################
parser = argparse.ArgumentParser(description='View that combine two table/view') 
parser.add_argument('--database', '-b', type = str, help = "database to connect to")
parser.add_argument('--host', '-o', type=str, required=False, help="type of database host, localhost by default")
parser.add_argument('--table', '-t', type = str, required=False, help = "name of the table required, all of them if not precised")
args = parser.parse_args()
###############################################################################################

try:
    conn = mc.connect(host=args.host,
    user=config.BD_USER,
    password=config.BD_PASSWORD) 

except mc.Error as err:
    print(err)

else:  
    rootpath = Path(__file__).resolve().parent.parent
    path = rootpath / f"data/tables"
    cursor = conn.cursor()
    cursor.execute(f"USE {args.database}")

    if args.table is not None :
        with open(path / f"{args.table}.tsv", "w") as tsv:
            nb_atribute = 0
            cursor.execute(f"DESCRIBE {args.table}")
            for el in cursor:
                nb_atribute += 1
            cursor.execute(f"SELECT * FROM {args.table}")
            for el in cursor:
                for i in range(nb_atribute):
                    tsv.write(f"{el[i]}\t")
                tsv.write("\n")
    else : 
        cursor.execute(f"SHOW TABLES")
        tables = []
        for el in cursor:
            tables.append(el[0])
        for el in tables:
            with open(path / f"{el}.tsv", "w") as tsv:
                nb_atribute = 0
                cursor.execute(f"DESCRIBE {el}")
                for x in cursor:
                    nb_atribute += 1
                cursor.execute(f"SELECT * FROM {el}")
                for y in cursor:
                    for i in range(nb_atribute):
                        tsv.write(f"{y[i]}\t")
                    tsv.write("\n")
                    
    print("Done : .tsv files available in data/tables")
                    
    