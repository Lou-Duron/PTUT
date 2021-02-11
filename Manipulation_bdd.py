#coding:utf-8

#Attention a l'historiquequeque joietsrfeshfus

import mysql.connect as mc

try:
    conn = mc.connect(host = '', database = '', user = '', password='')
    cursor = conn.cursor()

    req = 'SELECT * FROM archee' #exemple requete
    cursor.execute(req)

    ins = "INSERT INTO archee VALUES (%s, %s, %s)" # exemple insertion
    val = ('exid', 'extruc', 85) # insertion d'un archee

    cursor.execute(ins, val)
    conn.commit #commit

    archeelist = cursor.fetchall()

    for arche in archeelist:
        print('Identifiant : {}'.format(archee[0]))

except mc.Error as err: # si la connexion échoue
    print(err)

finally: # s'execute de toute facon
    if(conn.is_connected()):
        cursor.close() # ferme le cursor
        conn.close() # ferme la connexion
