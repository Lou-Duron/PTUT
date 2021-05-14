#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import requests
import random
import argparse
from pathlib import Path

################################################################################################
parser = argparse.ArgumentParser(description='Parser_iTOL') 
parser.add_argument('--database', '-b', type = str, help = "database to connect to")
args = parser.parse_args()
###############################################################################################
try:
    conn = mc.connect(host='localhost',
    user=config.BD_USER,
    password=config.BD_PASSWORD) 

except mc.Error as err:
    print(err)

else:  
    rootpath = Path(__file__).resolve().parent.parent
    path = rootpath / "analysis/Visualization"
    cursor = conn.cursor()
    dico = {}
    dicoName = {}
    values = []
    colors = []
    cursor.execute(f"USE {args.database}")
    cursor.execute("SELECT id_uniprot, id_cog FROM proteins_cog")
    for el in cursor:
        if el[1]!="NA":
            if el[0] not in dico.keys():
                dico[el[0]]=[]
            dico[el[0]].append(el[1])

    for ID in dico.keys():
        firstline = False
        url_arcog = "https://www.uniprot.org/uniprot/"+ID+".txt"
        arcog_response = requests.get(url_arcog)
        arcog_response.raise_for_status()
        Embl_file = arcog_response.text.split("\n")
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
                    if name not in dicoName.keys():
                        print(name)
                        dicoName[name] = []
                    for id in dico[ID]:
                        if id not in dicoName[name]:
                            dicoName[name].append(id)

    for el in range(len(values)):
        colors.append("rgb("+str(random.randrange(255))+","+str(random.randrange(255))+","+str(random.randrange(255))+")")

    with open(path + "/NCBI_tree.txt", "w") as tree:
        with open(path + "/iTOL_annotation.txt", "w") as anot:
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
            for i in dicoName.keys():
                tree.write(i + "\n")
                anot.write(i)
                for j in values:
                    if j in dicoName[i]:
                        anot.write("\t"+"50")
                    else:
                        anot.write("\t"+"0")
                anot.write("\n")