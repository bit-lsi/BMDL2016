#!/usr/bin/env python3

""" Test module installations """

import sys
import json
import logging
import json
import os
import unittest
import importlib

log = logging.getLogger()

BASE = "BUG_FREE_EUREKA_BASE"

class TestBugFreeEureka(unittest.TestCase):
    def setUp(self):
        self.base = os.environ[BASE]
    
    def test_env(self):
        if BASE not in os.environ:
            print("{} not on PATH".format(BASE))
    
    def test_reqs(self):
        with open(os.path.join(self.base, 'requirements.txt')) as requirements:
            for line in requirements:
                req = line.strip()
                try:
                    importlib.import_module(req)
                except Exception as e:
                    print("Unable to import {}\n  Run: pip3 install {}".format(req, req))
                else:
                    print("Successfully imported {}".format(req))

    def test_secrets(self):
        if not os.path.exists(os.path.join(self.base, 'secrets.json')):
            print('./secrets.json not found')

    def test_db(self):
        try:
            pymysql = importlib.import_module('pymysql')
        except:
            print('unable to import pymysql')
            
        with open(os.path.join(self.base, "secrets.json")) as f:
            secrets = json.load(f)

        connection_params = secrets["test_db"]

        with pymysql.connect(**connection_params) as cursor:
            print('Successfully connected to database {}'.format(connection_params))
            cursor.execute("select 'Successfully queried database'")
            print(*cursor.fetchone())
    

if __name__ == '__main__':
    unittest.main()
