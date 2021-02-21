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

dico = {}
with open(args.heli_file, "r") as fh:  # reading tsv entry file using args module
    tsv = csv.reader(fh, delimiter="\t")
    for line in tsv:
        if line[0] not in dico:
            dico[line[0]] = line[1]  # Adding each line into a dictionary containing the organism id in key and the
            # protein id for value. This is collected from the helicase file we've had from Petra.


with open(args.out_file, "w") as fh2:  # openning writing file
    csv_writer = csv.writer(fh2, delimiter="\t")

    for value in dico.values():  # for each value in the dict, search corresponding eggnog
        url = 'https://www.uniprot.org/uploadlists/'  # from here to the "response.decode('utf-8') it's a code i got
        # from https://www.uniprot.org/help/api_idmapping.

        params = {'from': 'ACC', 'to': 'EGGNOG_ID', 'format': 'tab', 'query': value}  # query = values in the dico

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        csv_writer.writerow(response.decode('utf-8'))

"""
Update, where i am :
argparse : entry file is the tsv file from petra, correctly read no problem for that, maybe i'll have to read and write
at the same time to avoid creating a big dict but the dict is really read really fast so we will see.
The outfile is not ready yet. I managed to have eggnog id from protein id ( petra's file ) but the page setting is not 
correct
"""