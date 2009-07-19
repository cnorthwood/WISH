#!/usr/bin/env python

class state:
    
    _auths = dict()
    _connection = None
    
    def __init__(self, connection):
        self._connection = connection
    
    def authenticate(self, numeric, acname):
        self._auths[numeric] = acname
    
    def getAccountName(self, numeric):
        return self._auths[numeric]
    
    def sendLine(self, client, command, args):
        self._connection.sendLine(client, command, args)
    
    def getServerID(self):
        return self._connection.numericID
    
    def getServerName(self):
        return self._connection.serverName
    
    def getAdminName(self):
        return self._connection.adminNick
    
    def getContactEmail(self):
        return self._connection.contactEmail