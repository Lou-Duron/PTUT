#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mc
from configurations import config
""" 
My Sql conenctor library may require configuration of environment to solve Library dependencies.
see ReadMe
"""
mydb = mc.connect(
  host="localhost",
  user=config.BD_USER,
  password=config.BD_PASSWORD
)
