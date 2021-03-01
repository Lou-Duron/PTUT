#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import urllib.parse
import urllib.request

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
parser.add_argument('--helicasefile', '-f', dest="heli_file", type=str,
                    help="tsv file containing CGBD id and associated helicase designated by its uniprot protein id")
parser.add_argument('--outfile', '-o', dest="out_file", type=str,
                    help="csv(or tsv) file containing ... to fill")

args = parser.parse_args()

dico_helicase = {}
with open(args.heli_file, "r") as fh:  # reading tsv entry file using args module
    tsv = csv.reader(fh, delimiter="\t")
    for line in tsv:
        if line[1] not in list(dico_helicase.values()):  # Check if the protein is not
            dico_helicase[line[0]] = line[1]  # Adding each line into a dictionary containing the organism id in key and
            # the protein id for value. This is collected from the helicase file we've had from Petra.

print(dico_helicase)


list_eggnog = []
list_of_list = []

with open(args.out_file, "w") as fh2:  # openning writing file
    csv_writer = csv.writer(fh2, delimiter="\t")

    for key in dico_helicase.keys():  # for each key in the dict, search corresponding eggnog to the value of the key
        url = 'https://www.uniprot.org/uploadlists/'  # from here to the "response.decode('utf-8') it's a code i got
        # from https://www.uniprot.org/help/api_idmapping.

        params = {'from': 'ACC', 'to': 'EGGNOG_ID', 'format': 'tab', 'query': dico_helicase[key]}  # query = values in
        # the dico_helic

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()

        list_eggnog.append(key)
        list_eggnog.append(dico_helicase[key])
        list_eggnog.append((response.decode('utf-8').split('\t')[2])[:-2])  # if you want to understand this, try this :
        # test_list = []
        # test_list.append(response.decode('utf-8'))
        # print(test_list)


        list_of_list.append(list_eggnog)  # Creating a list of list, each list within the list of list contains the
        # returned arcog associated to value ( = protein id ) and the  value ( = protein id )

        list_eggnog = []  # empty the list to fill it with the next values.

    for el in list_of_list:
        print(el)
        csv_writer.writerow(el)  # writing all the lists in the list by rows


print(list_of_list)

"""
What's next ? Integrate mysql to python in order to write the right lines and add missing informations needed in the 
tables
"""