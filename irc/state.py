#!/usr/bin/env python

import time
import p10.parser
import threading

# IRC masks are very similar to UNIX filename pattern matching, so we can cheat and use the same algorithm
import fnmatch

class state:
    """ Holds the state for the current connection """
    
    _config = None
    users = dict()
    channels = dict()
    _servers = dict()
    maxClientNumerics = dict()
    _glines = dict()
    _jupes = dict()
    lock = None
    _callbacks = dict()
    
    def __init__(self, config):
        self.users = dict()
        self.channels = dict()
        self._config = config
        self._servers = dict()
        self._servers[self.getServerID()] = server(None, self.getServerID(), self.getServerName(), 262143, self.ts(), self.ts(), "P10", 0, [], "WISH on " + self.getServerName())
        self.maxClientNumerics = dict({self.getServerID(): 262143})
        self._glines = dict()
        self._jupes = dict()
        self.lock = threading.RLock()
        self._callbacks = dict()
    
    # Constants for Callbacks
    CALLBACK_NEWUSER = "NewUser"
    CALLBACK_QUIT = "Quit"
    CALLBACK_KILL = "Kill"
    CALLBACK_CHANGENICK = "ChangeNick"
    CALLBACK_NEWSERVER = "NewServer"
    CALLBACK_AUTHENTICATE = "Authenticate"
    CALLBACK_AWAY = "Away"
    CALLBACK_BACK = "Back"
    CALLBACK_CHANNELCREATE = "ChannelCreate"
    CALLBACK_CHANNELDESTROY = "ChannelDestroy"
    CALLBACK_CHANNELJOIN = "ChannelJoin"
    CALLBACK_CHANNELPART = "ChannelPart"
    CALLBACK_CHANNELPARTALL = "ChannelPartAll"
    CALLBACK_CHANNELPARTZOMBIE = "ChannelPartZombie"
    CALLBACK_CHANNELKICK = "ChannelKick"
    CALLBACK_CHANNELMODECHANGE = "ChannelModeChange"
    CALLBACK_CHANNELBANADD = "ChannelBanAdd"
    CALLBACK_CHANNELBANREMOVE = "ChannelBanRemove"
    CALLBACK_CHANNELBANCLEAR = "ChannelBanClear"
    CALLBACK_CHANNELOP = "ChannelOp"
    CALLBACK_CHANNELDEOP = "ChannelDeop"
    CALLBACK_CHANNELCLEAROPS = "ChannelClearOps"
    CALLBACK_CHANNELVOICE = "ChannelVoice"
    CALLBACK_CHANNELDEVOICE = "ChannelDevoice"
    CALLBACK_CHANNELCLEARVOICES = "ChannelClearVoices"
    CALLBACK_GLINEADD = "GlineAdd"
    CALLBACK_GLINEREMOVE = "GlineRemove"
    CALLBACK_INVITE = "Invite"
    CALLBACK_JUPEADD = "JupeAdd"
    CALLBACK_JUPEREMOVE = "JupeRemove"
    CALLBACK_REQUESTADMIN = "RequestAdmin"
    CALLBACK_REQUESTINFO = "RequestInfo"
    CALLBACK_REQUESTLUSERS = "RequestLusers"
    CALLBACK_REQUESTLINKS = "RequestLinks"
    
    def registerCallback(self, type, callbackfn):
        if type in self._callbacks:
            self._callbacks[type].append(callbackfn)
        else:
            self._callbacks[type] = [callbackfn]
    
    def _callback(self, type, args):
        if type in self._callbacks:
            for callback in self._callbacks[type]:
                callback(args)
    
    def getServerID(self):
        return self._config.numericID
    
    def getServerName(self):
        return self._config.serverName
    
    def getAdminName(self):
        return self._config.adminNick
    
    def getContactEmail(self):
        return self._config.contactEmail
    
    def serverExists(self, numeric):
        return numeric in self._servers
    
    def newServer(self, origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description):
        """ Add a new server """
        # TODO: More stringent checks - do we have a name clash?
        self.lock.acquire()
        try:
            if self.serverExists(numeric):
                raise StateError("Attempted to add a duplicate server")
            elif origin[1] != None:
                raise p10.parser.ProtocolError("User attempted to add a server")
            else:
                uplink = origin[0]
                if self.serverExists(uplink):
                    self._servers[numeric] = server(uplink, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description)
                    self.maxClientNumerics[numeric] = maxclient
                    self._servers[uplink].addChild(numeric)
                else:
                    raise StateError("Unknown server introduced a new server")
        finally:
           self.lock.release()
        self._callback(self.CALLBACK_NEWSERVER, (origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description))
    
    def getNextHop(self, dest):
        if dest[0] == self.getServerID():
            return None
        elif dest[0] in self._servers:
            return dest[0]
        else:
            for server in self._servers:
                if dest[0] in server.children:
                    return server.numeric
    
    def sendAdminInfo(self, origin, target):
        if self.userExists(origin):
            if target[1] == None:
                self._callback(self.CALLBACK_REQUESTADMIN, (origin, target))
            else:
                raise p10.parser.ProtocolError("Admin information can only be requested from servers")
        else:
            raise StateError("Received a request for admin info from a non-existant user")
    
    def sendServerInfo(self, origin, target):
        if self.userExists(origin):
            if target[1] == None:
                self._callback(self.CALLBACK_REQUESTINFO, (origin, target))
            else:
                raise p10.parser.ProtocolError("Server information can only be requested from servers")
        else:
            raise StateError("Received a request for server info from a non-existant user")
    
    def sendLusersInfo(self, origin, target, dummy):
        if self.userExists(origin):
            if target[1] == None:
                self._callback(self.CALLBACK_REQUESTLUSERS, (origin, target, dummy))
            else:
                raise p10.parser.ProtocolError("Luser information can only be requested from servers")
        else:
            raise StateError("Received a request for Luser info from a non-existant user")
    
    def sendLinksInfo(self, origin, target, mask):
        if self.userExists(origin):
            if target[1] == None:
                self._callback(self.CALLBACK_REQUESTLINKS, (origin, target, mask))
            else:
                raise p10.parser.ProtocolError("Links information can only be requested from servers")
        else:
            raise StateError("Received a request for links info from a non-existant user")
    
    def ts(self):
        """ Returns our current timestamp """
        return int(time.time())
    
    def userExists(self, numeric):
        """ Check if the user is known to us """
        return numeric in self.users
    
    def nick2numeric(self, nick):
        for user in self.users:
            if nick == self.users[user].nickname:
                return user
    
    def newUser(self, origin, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname):
        """ Change state to include a new user """
        # TODO: Do we have a name clash?
        self.lock.acquire()
        try:
            if self.serverExists(origin[0]):
                if origin[1] == None:
                    if self.userExists(numeric):
                        raise StateError("Numeric collision - attempting to create second user with numeric we already know")
                    else:
                        self.users[numeric] = user(numeric, nickname, username, hostname, modes, ip, hops, ts, fullname)
                else:
                    raise p10.parser.ProtocolError("Only servers can create users")
            else:
                raise StateError("A non-existant server tried to create a user")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_NEWUSER, (origin, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname))
    
    def quit(self, numeric, reason):
        self.lock.acquire()
        try:
            if self.userExists(numeric):
                for channel in self.users[numeric].channels:
                    self.channels[channel].part(numeric)
                    self._cleanupChannel(channel)
                del self.users[numeric]
            else:
                raise StateError("Unknown user tried to quit")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_QUIT, (numeric, reason))
    
    def kill(self, origin, target, path, reason):
        if target[0] == self.getServerID():
            self.quit(target, "Killed (" + reason + ")")
        else:
            self._callback(self.CALLBACK_KILL, (origin, target, [self._servers[self.getNextHop(origin)].name] + path, reason))
    
    def changeNick(self, origin, numeric, newnick, newts):
        """ Change the nickname of a user on the network """
        # TODO: More stringent checks on new nickname, i.e., is it valid/already in use?
        self.lock.acquire()
        try:
            if self.userExists(numeric):
                self.users[numeric].nickname = newnick
                self.users[numeric].ts = newts
            else:
                raise StateError('Nick change attempted for unknown user')
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANGENICK, (origin, numeric, newnick, newts))
    
    def authenticate(self, origin, numeric, acname):
        """ Authenticate a user """
        self.lock.acquire()
        try:
            if origin[1] == None:
                if self.serverExists(origin[0]):
                    if self.userExists(numeric):
                        self.users[numeric].auth(acname)
                    else:
                        raise StateError("Authentication state change received for unknown user")
                else:
                    raise StateError("Authentication from unknown server")
            else:
                raise p10.parser.ProtocolError("Only servers can change state")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_AUTHENTICATE, (origin, numeric, acname))
    
    def getAccountName(self, numeric):
        """ Get the account name for a user. Blank if not authenticated. """
        return self.users[numeric].account
    
    def setAway(self, numeric, reason):
        """ Mark a user as being away. Reason must be non-empty """
        self.lock.acquire()
        try:
            if reason == "":
                raise StateError("Attempted to set an empty away reason")
            if self.userExists(numeric):
                self.users[numeric].away_reason = reason
            else:
                raise StateError("Attempted to mark a user as away who does not exist")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_AWAY, (numeric, reason))
    
    def setBack(self, numeric):
        """ Mark a user as no longer being away """
        self.lock.acquire()
        try:
            if self.userExists(numeric):
                self.users[numeric].away_reason = None
            else:
                raise StateError("Attempted to mark a user as not away who does not exist")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_BACK, (numeric))
    
    def createChannel(self, origin, name, ts):
        """ Create a channel. Returns false if the new channel is invalid (i.e., is newer than one already known about) """
        # TODO: More stringent checks on whether or not this channel can be created (i.e., is badchan'd or juped)
        create_success = False
        callback = False
        oldusers = []
        self.lock.acquire()
        try:
            if self.userExists(origin):
                # Channel already exists
                if name in self.channels:
                    # If our channel is older, disregard.
                    # If they're both the same, add new user as op
                    if self.channels[name].ts == ts:
                        self.joinChannel(origin, origin, name, ["o"], ts)
                        create_success = True
                        callback = False
                    # Their channel is older, overrides ours and merge users
                    elif self.channels[name].ts > ts:
                        self.channels[name].ts = ts
                        self.clearChannelOps(origin, name)
                        self.clearChannelVoices(origin, name)
                        self.clearChannelBans(origin, name)
                        for mode in self.channels[name].modes:
                            if mode[1] != False:
                                self.changeChannelMode(origin, name, ("-" + mode[0], None))
                        self.joinChannel(origin, origin, name, ["o"], ts)
                        create_success = True
                        callback = False
                else:
                    self.channels[name] = channel(name, ts)
                    self.channels[name].join(origin, ["o"])
                    self.users[origin].join(name)
                    callback = True
                    create_success = True
            else:
                raise StateError("Unknown entity attempted to create a channel")
        finally:
            self.lock.release()
        if callback:
            self._callback(self.CALLBACK_CHANNELCREATE, (origin, name, ts))
        return create_success
    
    def channelExists(self, name):
        """ Returns if a channel exists or not """
        return name in self.channels
    
    def joinChannel(self, origin, numeric, name, modes, ts=1270080000):
        """ A user joins a channel, with optional modes already set. If the channel does not exist, it is created. """
        # TODO: More stringent checks on whether or not this user is allowed to join this channel
        self.lock.acquire()
        callback = False
        try:
            if self.userExists(numeric):
                if self.channelExists(name):
                    self.channels[name].join(numeric, modes)
                    self.users[numeric].join(name)
                    callback = True
                else:
                    self.createChannel(numeric, name, ts)
            else:
                raise StateError("Unknown user attempted to join a channel")
        finally:
            self.lock.release()
        if callback:
            self._callback(self.CALLBACK_CHANNELJOIN, (origin, numeric, name, modes, ts))
            if "o" in modes:
                self._callback(self.CALLBACK_CHANNELOP, (origin, name, numeric))
            if "v" in modes:
                self._callback(self.CALLBACK_CHANNELVOICE, (origin, name, numeric))
    
    def _cleanupChannel(self, name):
        self.lock.acquire()
        try:
            if len(self.channels[name].users()) == 0 and len(self.channels[name].zombies) == 0:
                del self.channels[name]
                for user in self.users:
                    # Remove any invites that a user may have to this channel
                    if self.users[user].isInvited(name):
                        self.users[user].invites.remove(name)
        finally:
            self.lock.release()
    
    def partChannel(self, numeric, name, reason):
        """ A user parts a channel """
        self.lock.acquire()
        callbackZombie = True
        try:
            if self.userExists(numeric):
                if self.channelExists(name):
                    if self.channels[name].ison(numeric):
                        if numeric in self.channels[name].users():
                            callbackZombie = False
                        self.channels[name].part(numeric)
                        self.users[numeric].part(name)
                        self._cleanupChannel(name)
                    else:
                        raise StateError("User that was not on a channel attempted to leave it")
                else:
                    raise StateError("User tried to leave a channel that does not exist")
            else:
                raise StateError("Unknown user attempted to leave a channel")
        finally:
            self.lock.release()
        if callbackZombie:
            self._callback(self.CALLBACK_CHANNELPARTZOMBIE, (numeric, name))
        else:
            self._callback(self.CALLBACK_CHANNELPART, (numeric, name, reason))
    
    def destroyChannel(self, origin, channel, ts):
        callback = True
        self.lock.acquire()
        try:
            if self.channelExists(channel):
                if len(self.channels[channel].users()) == 0:
                    del self.channels[channel]
                else:
                    callback = False
        finally:
            self.lock.release()
        if callback:
            self._callback(self.CALLBACK_CHANNELDESTROY, (origin, channel, ts))
    
    def kick(self, origin, channel, target, reason):
        self.lock.acquire()
        bouncepart = False
        try:
            # Kick handling is weird. We zombify the user until we receive an upstream part
            if self.channelExists(channel):
                if self.channels[channel].ison(target):
                    self.channels[channel].kick(target)
                    if target[0] == self.getServerID():
                        bouncepart = True
                        self.channels[channel].part(target)
                        self.users[target].part(channel)
                        self._cleanupChannel(channel)
                else:
                    raise StateError("Kick received for a user that is not on the channel")
            else:
                raise StateError("Kick received for a user on an unknown channel")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELKICK, (origin, channel, target, reason))
        if bouncepart:
            self._callback(self.CALLBACK_CHANNELPARTZOMBIE, (target, channel))
    
    def partAllChannels(self, numeric):
        """ A user parts all channels """
        # Shallow copy to allow us to modify during loop
        self.lock.acquire()
        try:
            for channel in self.users[numeric].channels.copy():
                self.channels[channel].part(numeric)
                self.users[numeric].part(channel)
                self._cleanupChannel(channel)
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELPARTALL, (numeric))
    
    def changeChannelMode(self, origin, name, mode):
        """ Change the modes on a channel. Modes are tuples of the desired change (single modes only) and an optional argument, or None """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].changeMode(mode)
                else:
                    raise StateError("Attempted to change the modes on a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to change a channel mode")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELMODECHANGE, (origin, name, mode))
    
    def addChannelBan(self, origin, name, mask):
        """ Adds a ban to the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].addBan(mask)
                else:
                    raise StateError("Attempted to add a ban to a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to add a channel ban")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELBANADD, (origin, name, mask))
    
    def removeChannelBan(self, origin, name, ban):
        """ Removes a ban from the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].removeBan(ban)
                else:
                    raise StateError("Attempted to remove a ban from a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to remove a channel ban")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELBANREMOVE, (origin, name, ban))
    
    def clearChannelBans(self, origin, name):
        """ Clears all bans from the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].clearBans()
                else:
                    raise StateError("Attempted to clear bans from a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to clear channel bans")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELBANCLEAR, (origin, name))
    
    def op(self, origin, channel, user):
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(channel):
                    if self.channels[channel].ison(user):
                        self.channels[channel].op(user)
                    else:
                        raise StateError("Attempted to op a user that was not on the channel")
                else:
                    raise StateError("Attempted to op a user on a channel that does not exist")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELOP, (origin, channel, user))
    
    def deop(self, origin, channel, user):
        """ Deops a user from the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(channel):
                    if self.channels[channel].isop(user):
                        self.channels[channel].deop(user)
                    else:
                        raise StateError('Attempted to deop a user that was not op on the channel')
                else:
                    raise StateError('Attempted to deop from a channel that does not exist')
            else:
                raise StateError("An invalid entity attempted to deop a user")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELDEOP, (origin, channel, user))
    
    def clearChannelOps(self, origin, name):
        """ Clears all ops from the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].clearOps()
                else:
                    raise StateError("Attempted to clear ops from a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to clear channel ops")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELCLEAROPS, (origin, name))
    
    def voice(self, origin, channel, user):
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(channel):
                    if self.channels[channel].ison(user):
                        self.channels[channel].voice(user)
                    else:
                        raise StateError("Attempted to voice a user that was not on the channel")
                else:
                    raise StateError("Attempted to voice a user on a channel that does not exist")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELVOICE, (origin, channel, user))
    
    def devoice(self, origin, channel, user):
        """ Devoices a user from the channel. """
        self.lock.acquire()
        try:
            # TODO: More stringent checks on whether or not this user is allowed to make this mode change
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(channel):
                    if self.channels[channel].isvoice(user):
                        self.channels[channel].devoice(user)
                    else:
                        raise StateError('Attempted to devoice a user that was not op on the channel')
                else:
                    raise StateError('Attempted to devoice from a channel that does not exist')
            else:
                raise StateError("An invalid entity attempted to devoice a user")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELDEVOICE, (origin, channel, user))
    
    def clearChannelVoices(self, origin, name):
        """ Clears all voices from the channel. """
        # TODO: More stringent checks on whether or not this user is allowed to make this mode change
        self.lock.acquire()
        try:
            if self.userExists(origin) or (self.serverExists(origin[0]) and origin[1] == None):
                if self.channelExists(name):
                    self.channels[name].clearVoices()
                else:
                    raise StateError("Attempted to clear voices from a channel that does not exist")
            else:
                raise StateError("An invalid entity attempted to clear channel voices")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_CHANNELCLEARVOICES, (origin, name))
    
    def _cleanupGlines(self):
        """ Remove expired g-lines """
        # Make shallow copy of dictionary so we can modify it during iteration
        self.lock.acquire()
        try:
            for gline in self._glines.copy():
                # Remove expired g-lines
                if self._glines[gline][1] < self.ts():
                    del self._glines[gline]
        finally:
            self.lock.release()
    
    def addGline(self, origin, mask, target, expires, description):
        """ Add a g-line """
        # TODO: Check if origin can actually set g-lines
        if target == None or target == self.getServerID():
            self._glines[mask] = (description, expires)
        self._callback(self.CALLBACK_GLINEADD, (origin, mask, target, expires, description))
    
    def isGlined(self, host):
        """ Check if someone is g-lined """
        self.lock.acquire()
        try:
            self._cleanupGlines()
            for mask in self._glines:
                if fnmatch.fnmatch(host, mask):
                    return self._glines[mask]
                else:
                    return None
        finally:
            self.lock.release()
    
    def removeGline(self, origin, mask, target):
        """ Remove a g-line """
        # TODO: Check if origin can actually remove g-lines
        self.lock.acquire()
        try:
            if target == None or target == self.getServerID():
                # Make shallow copy of dictionary so we can modify it during iteration
                for gline in self._glines.copy():
                    # Remove any g-lines that match that mask
                    if fnmatch.fnmatch(gline, mask):
                        del self._glines[gline]
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_GLINEREMOVE, (origin, mask, target))
    
    def invite(self, origin, target, channel):
        """ Origin invites Target to Channel """
        # TODO: Check origin can actually send invites
        self.lock.acquire()
        try:
            if self.userExists(target):
                if self.channelExists(channel):
                    self.users[target].invite(channel)
                else:
                    raise StateError("Attempted to invite a user into a non-existant channel")
            else:
                raise StateError("Attempted to invite a non-existant user to a channel")
        finally:
            self.lock.release()
        self._callback(self.CALLBACK_INVITE, (origin, target, channel))
    
    def _cleanupJupes(self):
        for jupe in self._jupes.copy():
            if self._jupes[jupe][0] < self.ts():
                del self._jupes[jupe]
    
    def isJuped(self, server):
        self._cleanupJupes()
        if server in self._jupes:
            return self._jupes[server]
        else:
            return None
    
    def addJupe(self, origin, target, server, expire, reason):
        if target == None or target == self.getServerID():
            self._jupes[server] = (expire, reason)
        self._callback(self.CALLBACK_JUPEADD, (origin, target, server, expire, reason))
    
    def removeJupe(self, origin, target, server):
        if target == None or target == self.getServerID():
            self.lock.acquire()
            try:
                if server in self._jupes:
                    del self._jupes[server]
            finally:
                self.lock.release()
        self._callback(self.CALLBACK_JUPEREMOVE, (origin, target, server))

class user:
    """ Represents a user internally """
    
    numeric = None
    nickname = ""
    username = ""
    hostname = ""
    _modes = dict()
    channels = set()
    ip = 0
    fullname = ""
    account = ""
    hops = 0
    ts = 0
    away_reason = None
    invites = set()
    
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
        self.channels = set()
        self.invites = set()
    
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
    
    def join(self, channel):
        self.channels.add(channel)
        if self.isInvited(channel):
            self.invites.remove(channel)
    
    def part(self, channel):
        self.channels.remove(channel)
    
    def invite(self, channel):
        self.invites.add(channel)
    
    def isInvited(self, channel):
        return channel in self.invites

class channel:
    """ Represents a channel internally """
    
    name = ""
    ts = 0
    _users = dict()
    zombies = set()
    modes = dict()
    bans = []
    
    def __init__(self, name, ts):
        self.name = name
        self.ts = ts
        self._users = dict()
        self.zombies = set()
        self.modes = dict()
        self.bans = []
    
    def join(self, numeric, modes):
        """ Add a user to a channel """
        self._users[numeric] = set(modes)
    
    def part(self, numeric):
        """ A user is parting this channel """
        if numeric in self.zombies:
            self.zombies.remove(numeric)
        del self._users[numeric]
    
    def kick(self, numeric):
        self.zombies.add(numeric)
    
    def changeMode(self, mode):
        """ Change a single mode associated with this channel """
        if mode[0][0] == "+" and mode[1] == None:
            self.modes[mode[0][1]] = True
        elif mode[0][0] == "+" and mode[1] != None:
            self.modes[mode[0][1]] = mode[1]
        else:
            self.modes[mode[0][1]] = False
    
    def hasMode(self, mode):
        """ Return whether a channel has a mode (and if it's something with an option, what it is) """
        if mode in self.modes:
            return self.modes[mode]
        else:
            return False
    
    def clearBans(self):
        """ Clears bans from the channel """
        self.bans = []
    
    def addBan(self, mask):
        """ Adds a ban to the channel """
        self.bans.append(mask)
    
    def removeBan(self, mask):
        """ Removes a ban from the channel """
        for ban in self.bans:
            if fnmatch.fnmatch(ban, mask):
                self.bans.remove(ban)
    
    def ison(self, numeric):
        """ Returns whether a not a user is on a channel """
        return numeric in self._users
    
    def users(self):
        """ Return the list of users """
        r = self._users.copy()
        for z in self.zombies:
            del r[z]
        return r
    
    def isop(self, numeric):
        """ Check if a user is op on a channel """
        if self.ison(numeric):
            return "o" in self._users[numeric]
        else:
            return False
    
    def ops(self):
        ret = list()
        for user in self.users():
            if self.isop(user):
                ret.append(user)
        return ret
    
    def op(self, numeric):
        self._users[numeric].add("o")
    
    def deop(self, numeric):
        self._users[numeric].remove("o")
    
    def clearOps(self):
        for op in self.ops():
            self.deop(op)
    
    def isvoice(self, numeric):
        """ Check if a user is voice on a channel """
        if self.ison(numeric):
            return "v" in self._users[numeric]
        else:
            return False
    
    def voices(self):
        ret = list()
        for user in self.users():
            if self.isvoice(user):
                ret.append(user)
        return ret
    
    def voice(self, numeric):
        self._users[numeric].add("v")
    
    def devoice(self, numeric):
        self._users[numeric].remove("v")
    
    def clearVoices(self):
        for voice in self.voices():
            self.devoice(voice)

class server:
    """ Internally represent a server """
    numeric = 0
    origin = None
    name = ""
    maxclient = 0
    boot_ts = 0
    link_ts = 0
    protocol = ""
    hops = 0
    flags = set()
    description = ""
    children = set()
    
    def __init__(self, origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description):
        self.numeric = numeric
        self.origin = origin
        self.name = name
        self.maxclient = maxclient
        self.boot_ts = boot_ts
        self.link_ts = link_ts
        self.protocol = protocol
        self.hops = hops
        self.flags = set(flags)
        self.description = description
        self.children = set()
    
    def addChild(self, child):
        self.children.add(child)

class StateError(Exception):
    """ An exception raised if a state change would be impossible, generally suggesting we've gone out of sync """
    pass