#!/usr/bin/env python

class state:
    """ Holds the state for the current connection """
    
    _connection = None
    users = dict()
    
    def __init__(self, connection):
        self.users = dict()
        self._connection = connection
    
    def authenticate(self, numeric, acname):
        """ Authenticate a user """
        if self.userExists(numeric):
            self.users[numeric].auth(acname)
        else:
            raise StateError("Authentication state change received for unknown user")
    
    def getAccountName(self, numeric):
        """ Get the account name for a user. Blank if not authenticated. """
        return self.users[numeric].account
    
    def sendLine(self, client, command, args):
        """ Send a line """
        self._connection.sendLine(client, command, args)
    
    def getServerID(self):
        return self._connection.numericID
    
    def getServerName(self):
        return self._connection.serverName
    
    def getAdminName(self):
        return self._connection.adminNick
    
    def getContactEmail(self):
        return self._connection.contactEmail
    
    def userExists(self, numeric):
        """ Check if the user is known to us """
        return numeric in self.users
    
    def newUser(self, numeric, nickname, username, hostname, modes, ip, fullname):
        """ Change state to include a new user """
        self.users[numeric] = user(numeric, nickname, username, hostname, modes, ip, fullname)

class user:
    """ Represents a user internally """
    
    numeric = None
    nickname = ""
    username = ""
    hostname = ""
    _modes = dict()
    ip = 0
    fullname = ""
    account = ""
    
    def __init__(self, numeric, nickname, username, hostname, modes, ip, fullname):
        self.numeric = numeric
        self.nickname = nickname
        self.username = username
        self.hostname = hostname
        self._modes = dict()
        for mode in modes:
            self.changeMode(mode)
        self.ip = ip
        self.fullname = fullname
    
    def auth(self, account):
        """ Mark this user as authenticated """
        if self.account == "":
            self.account = account
        else:
            raise StateError("Authentication state change received for someone who is already authenticated")
    
    def changeMode(self, mode):
        """ Change a single mode associated with this user """
        if mode[0][0] == "+" and mode[1] == None:
            self._modes[mode[0][1]] = True
        elif mode[0][0] == "+" and mode[1] != None:
            self._modes[mode[0][1]] = mode[1]
        else:
            self._modes[mode[0][1]] = False
    
    def hasGlobalMode(self, mode):
        """ Return whether a user has a mode """
        if mode in self._modes:
            return self._modes[mode]
        else:
            return False

class StateError(Exception):
    """ An exception raised if a state change would be impossible, generally suggesting we've gone out of sync """
    pass