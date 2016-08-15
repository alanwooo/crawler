# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import, unicode_literals)

__all__ = ["getAuth", "httpsRequest"]

import sys
import pymongo

class mongodbHandler():
    def __init__(self, hostname, port)
        self.hostname = hostname
        self.port = port
        self.conn = None
        self.db = None
        self.coll = None
        self._getConn()

    def _getConn(self):
        try:
            self.conn = pymongo.MongoClient(self.hostname, self.port)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to the DB server : %s" % e
            sys.exit(1)
        if ! self.conn:
            print "Could not get the connection !"
            sys.exit(1)

    def getDB(self, dbname):
        self.db = self.conn[dbname]

    def getCollection(self, collname):
        self.coll = self.db[collname]

    def insertOneRepo(self, repo):
        try:
            self.coll.insert(repo, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError, e:
            print "Insert the repo %s to mongodb fail with : %s" % (repo['id'], e)
            sys.exit(1)

    def insertMultiRepos(self, repos):
        if ! repos:
            return None
        for repo in repos:
            self.insertOneRepo(repo)   
