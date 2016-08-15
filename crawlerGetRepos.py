# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import, unicode_literals)

import os
import time
import json
import traceback
import datetime
import ConfigParser

from lib.mongodbHandler import mongodbHandler as mongo
from lib.httpsRequest import *

SINCE = 0
REPOID = 'repo.id'

def saveProcess(*args):
    global SINCE
    if args:
        with open(REPOID, 'w+') as fd:
            fd.write(str(SINCE))
            fd.flush()
    else:
        with open(REPOID, 'r') as fd:
            SINCE = int(fd.read())

def readConf():
    config = ConfigParser.ConfigParser()
    config.read('./conf')
    username = config.get('info', 'username').strip()
    password = config.get('info', 'password').strip()
    if not ( username and password):
        print ("Please set the Username and Password in conf.")
    os.environ['USERNAME'] = username
    os.environ['PASSWORD'] = password

if os.path.isfile(REPOID):
    saveProcess()
else:
    with open(REPOID, 'w+') as fd:
        fd.write(str(SINCE))
        fd.flush()

readConf()
client = mongo('127.0.0.1', 27017)
client.getDB('github')
client.getCollection('repositories')
#client.getCollection('projects')

while True:
   try:
       repos = httpsRequest('/repositories', since = SINCE).json()
   except Exception as e:
       print ("Ignore exception :")
       traceback.print_exc()
       continue

   if not isinstance(repos, list):
       continue

   client.insertMultiRepos(repos)
   print ('%s' % SINCE)
   saveProcess(SINCE)

   SINCE = int(repos[-1]['id'])

