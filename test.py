#!/usr/bin/env python3

""" Test module installations """

import sys
import json
import logging
import pymysql

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log.warn(sys.version)

reqs = ["numpy", "pandas", "networkx", "sklearn", "pymysql"]

for req in reqs:
    try:
        __import__(req)
    except Exception as e:
        print("failure: {}".format(e))
    else:
        print("successfully imported {}".format(req))

with open("secrets.json") as f:
    secrets = json.load(f)

connection_params = secrets["test_db"]

with pymysql.connect(**connection_params) as cursor:
    cursor.execute("select 'successfully connected to/queried database'")
    res = cursor.fetchone()
    for col in res:
        print(col)
