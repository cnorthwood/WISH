#!/usr/bin/env python

import time

class state:
    """ Holds the state for the current connection """
    
    _connection = None
    users = dict()
    channels = dict()
    
    def __init__(self, connection):
        self.users = dict()
        self.channels = dict()
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
    
    def createChannel(self, name, ts):
        """ Create a channel. Returns false if the new channel is invalid (i.e., is newer than one already known about) """
        # Channel already exists
        if name in self.channels:
            # Our channel is older. Disregard.
            if self.channels[name].ts < ts:
                return False
            # They're both the same!
            elif self.channels[name].ts == ts:
                return True
            # Their channel is newer. Merge the 2 (but only users)
            else:
                # Get old users
                oldusers = dict.keys(self.channels[name].users)
                self.channels[name] = channel(name, ts)
                for user in oldusers:
                    self.joinChannel(name, user, [])
                return True
        else:
            self.channels[name] = channel(name, ts)
            return True
    
    def channelExists(self, name):
        """ Returns if a channel exists or not """
        return name in self.channels
    
    def joinChannel(self, name, numeric, modes):
        """ A user joins a channel, with optional modes already set. If the channel does not exist, it is created. """
        if self.channelExists(name):
            self.channels[name].join(numeric, modes)
        else:
            self.createChannel(name, self.ts())
            self.channels[name].join(numeric, list(set(modes + ["o"])))
    
    def changeChannelMode(self, name, mode):
        """ Change the modes on a channel. Modes are tuples of the desired change (single modes only) and an optional argument, or None """
        if self.channelExists(name):
            self.channels[name].changeMode(mode)
        else:
            raise StateError("Attempted to change the modes on a channel that does not exist")
    
    def ts(self):
        """ Returns our current timestamp """
        return int(time.time())
    
    def addChannelBan(self, name, mask):
        if self.channelExists(name):
            self.channels[name].addBan(mask)
        else:
            raise StateError("Attempted to add a ban to a channel that does not exist")

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
        """ Return whether a user is away or not """
        if self.away_reason == None:
            return False
        else:
            return True

class channel:
    """ Represents a channel internally """
    
    name = ""
    ts = 0
    users = dict()
    _modes = dict()
    bans = []
    
    def __init__(self, name, ts):
        self.name = name
        self.ts = ts
        self.users = dict()
        self._modes = dict()
        self.bans = []
    
    def join(self, numeric, modes):
        """ Add a user to a channel """
        self.users[numeric] = modes
    
    def isop(self, numeric):
        """ Check if a user is op on a channel """
        return "o" in self.users[numeric]
    
    def changeMode(self, mode):
        """ Change a single mode associated with this channel """
        if mode[0][0] == "+" and mode[1] == None:
            self._modes[mode[0][1]] = True
        elif mode[0][0] == "+" and mode[1] != None:
            self._modes[mode[0][1]] = mode[1]
        else:
            self._modes[mode[0][1]] = False
    
    def hasMode(self, mode):
        """ Return whether a channel has a mode (and if it's something with an option, what it is) """
        if mode in self._modes:
            return self._modes[mode]
        else:
            return False
    
    def addBan(self, mask):
        """ Adds a ban to the channel """
        self.bans.append(mask)

class StateError(Exception):
    """ An exception raised if a state change would be impossible, generally suggesting we've gone out of sync """
    pass