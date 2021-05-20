#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
import argparse
import csv
import re
from configurations import config
from pathlib import Path
import requests
import time


################################################################################################
parser = argparse.ArgumentParser(description='Add mapped arcogs to database and remove previous results')
parser.add_argument('--database', '-b', type=str, help="database to connect to")
parser.add_argument('--host', '-o', type=str, required=False, help="type of database host, localhost by default")
parser.add_argument('--arcogs', '-a', type=str, required=False, help="tsv file with id_cogs descriptions and type from "
                                                                     "eggnog")
parser.add_argument('--suffix', '-s',  type=str, required=True, help="the name you want to give to your table")
parser.add_argument('--mapper', '-m', type=str, required=False, help="your arcog file from the eggnog mapper")
parser.add_argument('--helicasefile', '-f', type=str, required=False,
                    help="tsv file with CGBD id associated to uniprot protein id ")
parser.add_argument('--drop', '-d', required=False, action="store_true", help='drop all tables')
parser.add_argument('--name', '-n', type=str, required=False, default='obsolete',
                    help='filename of obsolete uniprot id (default obsolete.txt)')
args = parser.parse_args()
################################################################################################

rootpath = Path(__file__).resolve().parent.parent

def uniprot_connection(url):
    info = None
    while info is None: # retry if exception occurs 
        try: 
            info = requests.get(url)
            info.raise_for_status()  # If the response was successful, no Exception will be raised
            
        except Exception as err:
            print(f'An error occurred: {err}')  # Python 3.6
            print("retrying")
            time.sleep(1)
            info = None

    return info
    
try:
    # try connection the database
    conn = mc.connect(host=args.host,
                      user=config.BD_USER,  # BD_USER by default in directroy configurations
                      password=config.BD_PASSWORD)  # BD_PASSEWORD by default in directory configurations

except mc.Error as err:
    print(err)

else:
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {args.database};")
    cursor.execute(f"USE {args.database};")
    
    cursor.execute(
            f"CREATE TABLE IF NOT EXISTS `strain_proteins` (`ncbi_id` VARCHAR(30), `id_uniprot` "
            f"VARCHAR(30), `sequence` TEXT, PRIMARY KEY(`id_uniprot`));")

        
    if args.drop:
        cursor.execute(f"USE {args.database};")
        cursor.execute(f"DROP TABLE IF EXISTS `proteins_cog_{args.suffix}`;")
        cursor.execute(f"DROP VIEW IF EXISTS `paralogy_{args.suffix}`;")
        cursor.execute(f"DROP VIEW IF EXISTS `multiple_status_{args.suffix}`;")

    if args.mapper is not None:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `proteins_cog_{args.suffix}`(`id_uniprot` VARCHAR(30), `id_cog` "
                       f"VARCHAR(30), `e_value` FLOAT, `taxon_id` VARCHAR(30), `taxon_name` VARCHAR(100), "
                       f"`max_annotation_level` VARCHAR(100), `category` VARCHAR(5), `go` TEXT, `kegg_ko` VARCHAR(30),"
                       f"`kegg_pathway` VARCHAR(30), `kegg_module` VARCHAR(30), `kegg_reaction` VARCHAR(30), "
                       f"`kegg_rclass` VARCHAR(30), PRIMARY KEY(`id_uniprot`, `id_cog`, `taxon_id`));")
        
        nb_line = 0
        with open(args.mapper, "r") as fh:
            file = csv.reader(fh, delimiter="\t")
            for line in file: 
                if re.search("^[A-Z]", line[0]):
                    nb_line += 1

        with open(args.mapper, "r") as fh:
            tsv_emapper = csv.reader(fh, delimiter="\t")
            motif = re.compile(r"(arC.*@2157)")
            obsolete = []
            cpt = 0
            for line in tsv_emapper:
                if re.search("^[A-Z]", line[0]):  # and float(line[2]) < 0.05:  # Skip first lines and lines where
                    # e_value < 0.0
                    cpt += 1
                    print(f"In progress : {cpt}/{nb_line} proteins", end = "\r") 
                    id_uniprot = line[0]
                    e_value = line[2]
                    category = line[6]
                    go = line[9]
                    firstline = False
                    url = "https://www.uniprot.org/uniprot/" + id_uniprot + ".txt"
                    SQ = False
                    seq = ''
                    name = ''
                    Embl_file = uniprot_connection(url)
                    if Embl_file == '':
                        obsolete.append(id_uniprot)
                    else:
                        Embl_file = Embl_file.text.split("\n")         
                        for line_arc in Embl_file: #file
                            if(firstline == False):
                                if line_arc.startswith("OS"):
                                    firstline = True
                                    arcog = line_arc.split(" ")
                                    name = "'"
                                    for el in arcog:
                                        if el.startswith("("):
                                            break
                                        if el.startswith("sp"):
                                            break
                                        if el != "OS" and el != "":
                                            el = el.replace(".","")
                                            if(len(name)>1):
                                                name += " " + el
                                            else:
                                                name += el
                                    name.strip(" ")
                                    name += "'"
                            if SQ == True:
                                seq += line_arc.replace(' ', '').replace('\n', '').replace('//', '')
                            if line_arc.startswith("SQ"):
                                SQ = True

                        cursor.execute(f"INSERT IGNORE INTO strain_proteins "
                                        f"(ncbi_id, id_uniprot, sequence) VALUES (%s,%s,%s)",
                                        (name, id_uniprot, seq))


                    for el in line[4].split(","):
                        id_cog_mapper = re.search(".*@", el).group(0)[:-1]
                        taxon_id = re.search("@.*\|", el).group(0)[1:][:-1]
                        taxon_name = el.split("|")[1]
                        max_annotation_level = line[5].split("|")[0]
                        category = line[6]
                        kegg_ko = line[11]
                        kegg_pathway = line[12]
                        kegg_module = line[13]
                        kegg_reaction = line[14]
                        kegg_rclass = line[15]
                        if max_annotation_level == taxon_id:
                            max_annotation_level = "true"
                        else:
                            max_annotation_level = "false"
                        if go == "-":
                            cursor.execute(f"INSERT IGNORE INTO proteins_cog_{args.suffix} (id_uniprot, id_cog, e_value,"
                                           f" taxon_id, taxon_name, max_annotation_level, category, go, kegg_ko, "
                                           f"kegg_pathway, kegg_module, kegg_reaction, kegg_rclass) "
                                           f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                           (id_uniprot, id_cog_mapper, e_value, taxon_id, taxon_name,
                                            max_annotation_level, category, 'NA', kegg_ko, kegg_pathway, kegg_module,
                                            kegg_reaction, kegg_rclass))
                        else:
                            cursor.execute(f"INSERT IGNORE INTO proteins_cog_{args.suffix} (id_uniprot, id_cog, e_value,"
                                           f" taxon_id, taxon_name, max_annotation_level, category, go, kegg_ko, "
                                           f"kegg_pathway, kegg_module, kegg_reaction, kegg_rclass) "
                                           f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                           (id_uniprot, id_cog_mapper, e_value, taxon_id, taxon_name,
                                            max_annotation_level, category, go, kegg_ko, kegg_pathway, kegg_module,
                                            kegg_reaction, kegg_rclass))
        
        obsolete_path = rootpath / f"analysis/results/{args.name}.txt"
        obsolete_file = open(obsolete_path, "w")
        for proteins in obsolete:
            obsolete_file.write(proteins + "\n")
        obsolete_file.close()

    if args.helicasefile is not None:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS `proteins_cog_{args.suffix}`(`id_uniprot` VARCHAR(30),`id_cog` VARCHAR(100),"
            f"PRIMARY KEY(`id_uniprot`, `id_cog`));")
    
        nb_line = 0
        with open(args.helicasefile, "r") as fh:
            tsv_helicases = csv.reader(fh, delimiter="\t")
            for line in tsv_helicases: 
                nb_line += 1

        with open(args.helicasefile, "r") as fh:  # reading tsv entry file using args module
            cpt = 0
            tsv_helicases = csv.reader(fh, delimiter="\t")
            obsolete = []
            for line in tsv_helicases:  # File with uniprot id and CBI id
                cpt += 1
                print(f"In progress : {cpt}/{nb_line} proteins", end = "\r")
                id_uniprot = line[1]
                # Arcogs retrieval
                arcogs = []
                SQ = False
                seq = ''
                name = ''
                firstline = False
                url_arcog = "https://www.uniprot.org/uniprot/" + id_uniprot + ".txt"
                Embl_file = uniprot_connection(url_arcog)
                if Embl_file == '':
                    obsolete.append(id_uniprot)
                else:
                    Embl_file = Embl_file.text.split("\n")         
                    for line_arc in Embl_file:  # file
                        if(firstline == False):
                            if line_arc.startswith("OS"):
                                firstline = True
                                arcog = line_arc.split(" ")
                                name = "'"
                                for el in arcog:
                                    if el.startswith("("):
                                        break
                                    if el.startswith("sp"):
                                        break
                                    if el != "OS" and el != "":
                                        el = el.replace(".","")
                                        if(len(name)>1):
                                            name += " " + el
                                        else:
                                            name += el
                                name.strip(" ")
                                name += "'"   
                        if SQ == True:
                            seq += line_arc.replace(' ', '').replace('\n', '').replace('//', '')
                        if line_arc.startswith("SQ"):
                            SQ = True
                        
                        #arcog retrieval
                        if line_arc.startswith("DR   eggNOG"):
                            arcog = line_arc.split("; ")
                            arcogs.append(arcog[1])
                    if arcogs:
                        for el in arcogs:
                            cursor.execute(f"INSERT IGNORE INTO proteins_cog_{args.suffix} (id_uniprot, id_cog) "
                                        f"VALUES (%s,%s)", (id_uniprot, el))
                        conn.commit()
                    else:
                        cursor.execute(f"INSERT IGNORE INTO proteins_cog_{args.suffix} "
                                    f"(id_uniprot, id_cog) VALUES (%s,%s)", (id_uniprot, 'NA'))
                        conn.commit()

                        # Instertion for proteins with no cog
                        # Since NULL is not authorized as primary key, string 'NA' is used
                    
                    cursor.execute(f"INSERT IGNORE INTO strain_proteins "
                                f"(ncbi_id, id_uniprot, sequence) VALUES (%s,%s,%s)",
                                (name, id_uniprot, seq))        


        obsolete_path = rootpath / f"analysis/results/{args.name}.txt"
        obsolete_file = open(obsolete_path, "w")
        for proteins in obsolete:
            obsolete_file.write(proteins + "\n")
        obsolete_file.close()

        conn.commit()

    if args.arcogs is not None:
        cursor.execute(f"DROP TABLE IF EXISTS `cog`;")
        cursor.execute("CREATE TABLE IF NOT EXISTS `cog`(`id_cog` VARCHAR(30) UNIQUE, `category` VARCHAR(100), "
                       "`description` TEXT, PRIMARY KEY(`id_cog`));")
        with open(args.arcogs, "r") as fa:  # Reading of cog description
            tsv_arcogs = csv.reader(fa, delimiter="\t")
            for line in tsv_arcogs:
                if line[3] == "":
                    cursor.execute("INSERT IGNORE INTO cog (id_cog, category, description) VALUES (%s,%s ,%s)",
                                   (line[1], line[2], None))
                    conn.commit()

                else:
                    cursor.execute("INSERT IGNORE INTO cog (id_cog, category, description) VALUES (%s,%s ,%s)",
                                   (line[1], line[2], line[3]))
                    conn.commit()

    # Views
    cursor.execute(
        f"CREATE VIEW multiple_status_{args.suffix} AS SELECT id_uniprot, count(*) AS multiple "
        f"FROM proteins_cog_{args.suffix} GROUP BY id_uniprot;")  # Proteins with multiple cogs associated
    conn.commit()

    cursor.execute(f"CREATE VIEW paralogy_{args.suffix} AS SELECT id_cog, COUNT(DISTINCT(ncbi_id)) AS strain_count, "
                   f"count(id_uniprot) as proteins_count FROM proteins_cog_{args.suffix} NATURAL JOIN "
                   f"strain_proteins GROUP BY id_cog;")
    conn.commit()

    # strain and protein cog by cog

    if conn.is_connected():
        cursor.close()  # close cursor
        conn.close()  # close connection
