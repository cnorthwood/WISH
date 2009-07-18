#!/usr/bin/env python

class state():
    
    _auths = dict()
    
    def authenticate(self, numeric, acname):
        self._auths[numeric] = acname
    
    def getAccountName(self, numeric):
        return self._auths[numeric]