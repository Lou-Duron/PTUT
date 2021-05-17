#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
import requests
import random
import time
from pathlib import Path

try:
    conn = mc.connect(host="localhost",
    user=config.BD_USER,
    password=config.BD_PASSWORD) 

except mc.Error as err:
    print(err)

else:  
    cursor = conn.cursor()
    cursor.execute(f"USE ptut")
    cursor.execute("CREATE VIEW data AS SELECT (u.id_uniprot,u.id_cog,e.id_uniprot,e.id_cog_mapper) FROM proteins_cog u, proteins_cog_mapper e WHERE u.id_uniprot = e.id_uniprot")


    