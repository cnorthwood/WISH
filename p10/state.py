#!/usr/bin/env python

class state():
    
    _auths = dict()
    _connection = None
    
    def __init__(self, connection):
        self.connection = connection
    
    def authenticate(self, numeric, acname):
        self._auths[numeric] = acname
    
    def getAccountName(self, numeric):
        return self._auths[numeric]