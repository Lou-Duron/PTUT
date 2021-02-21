#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""The purpose of this python file is to parse data obtained from Petra's team, containing uniprot id of SF2 helicases
and the associated CGBD id of archaea in which the helicase has been found. Associated with the members.tsv file obtaine
directly from the EggNog database
"""

import argparse
import csv

parser = argparse.ArgumentParser(description='Permet de parser')  # to precise
parser.add_argument('--helicasefile', '-f', dest="heli_file", type=str,
                    help="tsv file containing CGBD id and associated helicase designated by its uniprot id")
parser.add_argument('--outfile', '-o', dest="out_file", type=str,
                    help="csv(or tsv) file containing ... to fill")


# parser.add_argument('--verbose', '-v', action="store_true", default=False,
#                    help="le fichier au format fasta à lire")

args = parser.parse_args()

"""with open(args.heli_file, "r") as fh:
    for ligne in fh:
        print(ligne)
        break
"""
# I'd like to gather the delimiter ( tab, comma etc ) to be able to work on both tsv or csv files without the need of
# the usr to specify which one.

# Necessity to associate each protein to its associated cog. 


y = []
with open(args.heli_file, "r") as fh:  # reading tsv entry file using args module
    tsv = csv.reader(fh, delimiter="\t")
    for lines in tsv:
        y.append(lines)

    with open(args.out_file, "w") as fh2:  # openning writing file
        csv_writer = csv.writer(fh2, delimiter="\t")

        for line in tsv:
            csv_writer.writerow(line)

print(y)