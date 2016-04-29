#!/usr/bin/env python3

""" Test module installations """

import sys
import psycopg2
import json
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log.warn(sys.version)

reqs = ["numpy", "pandas", "networkx", "sklearn"]

for req in reqs:
    try:
        __import__(req)
    except:
        print("failed to import {}".format(req))
    else:
        print("successfully imported {}".format(req))

with open("secrets.json") as f:
    secrets = json.load(f)

dsn = "dbname={} user={} port={}".format(secrets['dbname'], secrets['user'], secrets['port'])

with psycopg2.connect(dsn) as conn:
    with conn.cursor() as cursor:
        cursor.execute("select 'successfully connected to/queried database'")
        res = cursor.fetchone()
        for col in res:
            print(col)
