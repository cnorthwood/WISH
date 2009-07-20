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
    
    def newUser(self, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname):
        """ Change state to include a new user """
        if self.userExists(numeric):
            raise StateError("Numeric collision - attempting to create second user with numeric we already know")
        else:
            self.users[numeric] = user(numeric, nickname, username, hostname, modes, ip, hops, ts, fullname)
    
    def changeNick(self, numeric, newnick, newts):
        """ Change the nickname of a user on the network """
        if self.userExists(numeric):
            self.users[numeric].nickname = newnick
            self.users[numeric].ts = newts
        else:
            raise StateError('Nick change attempted for unknown user')
    
    def setAway(self, numeric, reason):
        if reason == "":
            raise StateError("Attempted to set an empty away reason")
        if self.userExists(numeric):
            self.users[numeric].away_reason = reason
        else:
            raise StateError("Attempted to mark a user as away who does not exist")
    
    def setBack(self, numeric):
        if self.userExists(numeric):
            self.users[numeric].away_reason = None
        else:
            raise StateError("Attempted to mark a user as not away who does not exist")

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
    hops = 0
    ts = 0
    away_reason = None
    
    def __init__(self, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname):
        self.numeric = numeric
        self.nickname = nickname
        self.username = username
        self.hostname = hostname
        self._modes = dict()
        for mode in modes:
            self.changeMode(mode)
        self.ip = ip
        self.hops = hops
        self.ts = ts
        self.fullname = fullname
        self.away_reason = None
    
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
            # If this mode is an authentication mode (i.e., in a burst)
            if mode[0][1] == "r":
                self.auth(mode[1])
        else:
            self._modes[mode[0][1]] = False
    
    def hasGlobalMode(self, mode):
        """ Return whether a user has a mode """
        if mode in self._modes:
            return self._modes[mode]
        else:
            return False
    
    def isAway(self):
        if self.away_reason == None:
            return False
        else:
            return True

class StateError(Exception):
    """ An exception raised if a state change would be impossible, generally suggesting we've gone out of sync """
    pass