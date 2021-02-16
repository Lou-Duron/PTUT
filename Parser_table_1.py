"""The purpose of this python file is to parse data obtained from Petra's team, containing uniprot id of SF2 helicases
and the associated CGBD id of archaea in which the helicase has been found. Associated with the members.tsv file obtaine
directly from the EggNog database
"""

import argparse
import csv

parser = argparse.ArgumentParser(description='Permet de parser')  # to precise
parser.add_argument('--helicasefile', '-f', dest="heli_file", type=str,
                    help="tsv file containing CGBD id and associated helicase designated by its uniprot id")

# arser.add_argument('--verbose', '-v', action="store_true", default=False,
#                    help="le fichier au format fasta à lire")

args = parser.parse_args()

with open(args.heli_file, "r") as fh:
    tsv = csv.reader(fh, delimiter="\t")
    for row in tsv:
        print(row)





