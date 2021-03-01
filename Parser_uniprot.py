#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
from Module import conversion

"""
The purpose of this file is to convert your tsv file containing proteins ids (uniprot) into the same file containing
gene ids (uniprot)
"""

"""
French help :
en gros le but de de parser c'est de parser le tsv de Petra pour avoir non pas les protein id mais les gene id car c'est
les gene id qui sont dans la table récupérée sur eggnog. https://www.uniprot.org/uploadlists/ c'est ça la table qui 
permettra de faire la correspondance entre protein id et gene id.
https://www.uniprot.org/help/api_idmapping
"""


parser = argparse.ArgumentParser(description='Parse tsv file containing protein names into gene names')  # to precise
parser.add_argument('--membersfile', '-m', dest="members_file", type=str,
                    help="tsv file containing -> to complete (see readme from eggnog)")
parser.add_argument('--helicasefile', '-f', dest="heli_file", type=str,
                    help="tsv file containing CGBD id and associated helicase designated by its uniprot protein id")
parser.add_argument('--outfile', '-o', dest="out_file", type=str,
                    help="csv(or tsv) file containing ... to fill")

args = parser.parse_args()

dico_members = {}
with open(args.members_file, "r") as fh:
    i = 0
    tsv_members = csv.reader(fh, delimiter="\t")
    for line in tsv_members:  # I have to gather all genes id from members file and search for its corresponding protein
        # id using the command line, i should probably use it as a module file ? -> test
        if line[1] not in dico_members.keys() and i < 50:  # Check if the COG is not already in the dictionary
            dico_members[line[1]] = {}  # if the COG isn't already in the dictionary, add a dictionary associated to the
            # cog key


            for el in line[4].split(','):  # for each line read associate to the cog key, a dictionary containing
                # organism and gene id.
                dico_members[line[1]][el.split('.')[0]] = el.split('.')[1]
                i += 1

print(dico_members)

"""
This dictionary is not currently used, will be in the next versions of this python file.
"""


dico_helicase = {}
with open(args.heli_file, "r") as fh:  # reading tsv entry file using args module
    tsv = csv.reader(fh, delimiter="\t")
    for line in tsv:
        if line[1] not in list(dico_helicase.values()):  # Check if the protein is not in the dicitionary
            dico_helicase[line[0]] = line[1]  # Adding each line into a dictionary containing the organism id in key and
            # the protein id for value. This is collected from the helicase file we've had from Petra.


list_eggnog = []
list_of_list = []

with open(args.out_file, "w") as fh2:  # openning writing file
    csv_writer = csv.writer(fh2, delimiter="\t")

    for key in dico_helicase.keys():  # for each key in the dict, search corresponding eggnog to the value of the key
        list_eggnog.append(key)
        list_eggnog.append(dico_helicase[key])
        list_eggnog.append(conversion(dico_helicase[key], 'ACC', 'EGGNOG_ID'))  # using the conversion function from
        # Module.py, read details in the Module.py file.

        list_of_list.append(list_eggnog)  # Creating a list of list, each list within the list of list contains the
        # returned arcog associated to value ( = protein id ) and the  value ( = protein id ). This is required to use
        # the writrow function ( see later ).

        list_eggnog = []  # empty the list to fill it with the next values.

    for el in list_of_list:
        csv_writer.writerow(el)  # writing all the lists in the list, by rows.

# Verification :
print(list_of_list)

"""
What's next ? Integrate mysql to python in order to write the right lines and add missing informations needed in the 
tables
"""