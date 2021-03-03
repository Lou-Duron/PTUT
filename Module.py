#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request

"""
This file contains the function 'convert' which permits to convert one identifier to its other corresponding. For 
exemple get the corresponding gene id to protein id. It is based on "database mapping service" from UniProt.
To use this function, simply enter what you want to convert, from what format to what format. And it will return what 
you asked to the desired format. 
Example : conversion(Q8ZZV0, 'ACC', 'EGGNOG_ID') 
Will return : arCOG01444
VERY IMPORTANT : all format can be found here https://www.uniprot.org/help/api_idmapping
"""


def conversion(initial, start, end):

    url = 'https://www.uniprot.org/uploadlists/'  # from here to the "response.decode('utf-8') it's a code i got
    # from https://www.uniprot.org/help/api_idmapping.

    params = {'from': start, 'to': end, 'format': 'tab', 'query': initial}

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()

    return(response.decode('utf-8').split('\t')[2])[:-1]
    # in fact, response.decode('utf-8') returns this ['From\tTo\nQ8ZZV0\tarCOG01444\n']
    # if you want to understand, try this :
    # test_list = []
    # test_list.append(response.decode('utf-8'))
    # print(test_list)
