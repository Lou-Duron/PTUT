#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import argparse
import csv
import re
from configurations import config
from pathlib import Path

################################################################################################
parser = argparse.ArgumentParser(description='Add mapped arcogs to database and remove previous results')
parser.add_argument('--database', '-b', type=str, help="database to connect to")
parser.add_argument('--arcogs', '-a', type=str, help="name of the arccog file")
parser.add_argument('--drop', '-d', required=False, action="store_true", help='drop all tables')
args = parser.parse_args()
################################################################################################

rootpath = Path(__file__).resolve().parent.parent

try:
    # try connection the database
    conn = mc.connect(host='localhost',
                      database=args.database,
                      user=config.BD_USER,  # BD_USER by default in directroy configurations
                      password=config.BD_PASSWORD)  # BD_PASSEWORD by default in directory configurations

except mc.Error as err:  # if connection failed
    print(err)

else:  # if connection succeed
    cursor = conn.cursor()

    arcogs = rootpath / f"analysis/results/{args.arcogs}"

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {args.database}")
    cursor.execute(f"USE {args.database}")

    if args.drop:
        cursor.execute("DROP TABLE IF EXISTS `proteins_cog_mapper`")

    cursor.execute("CREATE TABLE IF NOT EXISTS `proteins_cog_mapper`(`id_uniprot` VARCHAR(30),`id_cog_mapper` VARCHAR(30), "
                   "`taxon_id` VARCHAR(30), `taxon_name` VARCHAR(100), `max_annotation_level` VARCHAR(100), `category`"
                   "VARCHAR(5), `go` TEXT, PRIMARY KEY(`id_uniprot`, `id_cog_mapper`, `taxon_id`));")

    with open(arcogs, "r") as fh:
        tsv_emapper = csv.reader(fh, delimiter="\t")
        motif = re.compile(r"(arC.*@2157)")
        for line in tsv_emapper:
            if re.search("^[A-Z]", line[0]):  # and float(line[2]) < 0.05:  # Permet de skip les premières lignes et
                # celles dont la evalue non significative ( ce qui semble déjà être le cas pour toutes ).
                id_uniprot = line[0]
                # On supprime la ligne si elle est déjà présente, j'ai déja vérifié, toutes les lignes correspondantes
                # avant la modif avaient un NA.
                # Pour vérifier, quand c'est vide : requete select protein et cog != NA -> sensé rien renvoyer c'est que
                # c'est bon.
                category = line[6]
                go = line[9]

                for el in line[4].split(","):
                    id_cog_mapper = re.search(".*@", el).group(0)[:-1]
                    taxon_id = re.search("@.*\|", el).group(0)[1:][:-1]
                    taxon_name = el.split("|")[1]
                    max_annotation_level = line[5].split("|")[0]
                    if max_annotation_level == taxon_id:
                        max_annotation_level = "true"
                    else:
                        max_annotation_level = "false"
                    if go == "-":
                        cursor.execute("INSERT INTO proteins_cog_mapper (id_uniprot, id_cog_mapper, taxon_id, taxon_name, "
                                       "max_annotation_level, category, go) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                       (id_uniprot, id_cog_mapper, taxon_id, taxon_name, max_annotation_level,
                                        category, 'NA'))
                        print(id_uniprot, id_cog_mapper, taxon_id, taxon_name, max_annotation_level, category, 'NA')
                    else:
                        cursor.execute("INSERT INTO proteins_cog_mapper (id_uniprot, id_cog_mapper, taxon_id, taxon_name, "
                                       "max_annotation_level, category, go) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                       (id_uniprot, id_cog_mapper, taxon_id, taxon_name, max_annotation_level,
                                        category, go))
                        print(id_uniprot, id_cog_mapper, taxon_id, taxon_name, max_annotation_level, category, go)

    conn.commit()
    cursor.close()  # close cursor
    conn.close()  # close connection
