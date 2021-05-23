#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import random
import argparse
from pathlib import Path

################################################################################################
parser = argparse.ArgumentParser(description='Parser_iTOL, creates two files for results visualization') 
parser.add_argument('--database', '-b', type = str, help = "database to connect to")
parser.add_argument('--host', '-o', type=str, required=False, help="type of database host, localhost by default")
parser.add_argument('--suffix', '-s', type = str, help = "of the table to use")
parser.add_argument('--all', '-a', required=False, action="store_true", help='get all proteins, even if there is no COG associated')
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
    path = rootpath / "analysis/Visualization"
    cursor = conn.cursor()
    dico = {} # {species : [cogs]}
    values = []
    colors = []
    cursor.execute(f"USE {args.database}")
    cursor.execute(f"SELECT id_cog, ncbi_id FROM proteins_cog_{args.suffix} p, "
                   f"strain_proteins s WHERE p.id_uniprot = s.id_uniprot")
    
    if args.all:
        for el in cursor:
            if el[1] not in dico.keys():
                dico[el[1]]=[]
            dico[el[1]].append(el[0])
    else :
        for el in cursor:
            if el[0]!="NA":
                if el[1] not in dico.keys():
                    dico[el[1]]=[]
                dico[el[1]].append(el[0])

    for species in dico.keys():
        for arcog in dico[species]:
            if arcog not in values:
                values.append(arcog)  

    for el in range(len(values)):
        colors.append(f"rgb({str(random.randrange(255))},{str(random.randrange(255))},{str(random.randrange(255))})")

    with open(path / f"NCBI_tree_{args.suffix}.txt", "w") as tree:
        with open(path / f"iTOL_annotation_{args.suffix}.txt", "w") as anot:
            anot.write("DATASET_EXTERNALSHAPE"+"\n")
            anot.write("SEPARATOR TAB"+"\n")
            anot.write("DATASET_LABEL"+"\t"+"Annotation"+"\n")
            anot.write("COLOR"+"\t"+"#ff0000"+"\n")
            anot.write("FIELD_COLORS")
            for el in colors:
                anot.write("\t"+el)
            anot.write("\n")
            anot.write("FIELD_LABELS")
            for el in values:
                anot.write("\t"+str(el))
            anot.write("\n")
            anot.write("LEGEND_TITLE"+"\t"+"Legend"+"\n")
            anot.write("LEGEND_POSITION_X"+"\t"+"100"+"\n")
            anot.write("LEGEND_POSITION_Y"+"\t"+"100"+"\n")
            anot.write("LEGEND_SHAPES")
            for el in colors:
                anot.write("\t"+"1")
            anot.write("\n")
            anot.write("LEGEND_COLORS")
            for el in colors:
                anot.write("\t"+el)
            anot.write("\n")
            anot.write("LEGEND_LABELS")
            for el in values:
                anot.write("\t"+str(el))
            anot.write("\n")
            anot.write("LEGEND_SHAPE_SCALES")
            for el in colors:
                anot.write("\t"+"1")
            anot.write("\n")
            anot.write("DATA"+"\n")
            for species in dico.keys():
                tree.write(species + "\n")
                anot.write(species)
                for arc in values:
                    if arc in dico[species]:
                        anot.write("\t"+"50")
                    else:
                        anot.write("\t"+"0")
                anot.write("\n")
    print("Done : ")
    print(f"NCBI_tree_{args.suffix}.txt created")
    print(f"iTOL_annotation_{args.suffix}.txt created")
