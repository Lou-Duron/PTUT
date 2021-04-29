#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import csv
import re

try:
    # try connection the database
    conn = mc.connect(host='localhost',
                      database='ptut',
                      user=config.BD_USER,  # BD_USER by default in directroy configurations
                      password=config.BD_PASSWORD)  # BD_PASSEWORD by default in directory configurations

except mc.Error as err:  # si la connexion échoue
    print(err)

else:  # si le connexion réussie
    cursor = conn.cursor()

    with open("results/arcogs_results.fa.emapper (copie).annotations", "r") as fh:
        tsv_emapper = csv.reader(fh, delimiter="\t")
        i = 0
        motif = re.compile(r"(arC.*@2157)")
        for line in tsv_emapper:
            if re.search("^[A-Z]", line[0]):
                protein = line[0]
                # On supprime la ligne si elle est déjà présente, j'ai déja vérifié, toutes les lignes correspondantes
                # avant la modif avaient un NA.
                # Pour vérifier, quand c'est vide : requete select protein et cog != NA -> sensé rien renvoyer c'est que
                # c'est bon.
                cursor.execute("""DELETE FROM proteins_cog WHERE id_uniprot= %s """, (protein,))

                cog_list = []
                for el in line[4].split(","):
                    cog = re.search(".*@", el).group(0)[:-1]
                    if cog not in cog_list:
                        cog_list.append(cog)
                for cog in cog_list:
                    i += 1
                    cursor.execute("INSERT INTO proteins_cog (id_uniprot, id_cog) VALUES (%s,%s)", (protein, cog))

    print("Nombre de lignes ajoutées : ", i)

    conn.commit()
    cursor.close()  # close cursor
    conn.close()  # close connection
