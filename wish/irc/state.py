"""
WISH - the WorldIRC Service Host

Maintaining server state

Copyright (c) 2009-2011, Chris Northwood
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Chris Northwood nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# IRC masks are very similar to UNIX filename pattern matching, so we can cheat
# and use the same algorithm
from collections import defaultdict, namedtuple
import fnmatch
import time

from wish.p10.parser import ProtocolError

class State():
    """
    Holds the state for the current connection
    """
    
    #
    # Configuration of this server
    #
    
    def __init__(self, config):
        """
        Set up this state as a particular instance of an IRC server with the
        defined configuration
        """
        
        self.users = dict()
        self.channels = dict()
        self._config = config
        self.servers = {
            self.server_id: Server(
                None,
                self.server_id,
                self.server_name,
                262143,
                self.ts,
                self.ts,
                "P10",
                0,
                [],
                "WISH on " + self.server_name)
        }
        self.max_client_numerics = {
            self.server_id: 262143
        }
        
        self._glines = dict()
        self._jupes = dict()
        self._callbacks = defaultdict(list)
    
    @property
    def server_id(self):
        return self._config.numeric_id
    
    @property
    def server_name(self):
        return self._config.server_name
    
    @property
    def server_description(self):
        return self._config.server_description
    
    @property
    def admin_name(self):
        return self._config.admin_nick
    
    @property
    def contact_email(self):
        return self._config.contact_email
    
    def request_admininfo(self, origin, target):
        """
        Handle with incoming requests for admin info
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTADMIN, origin, target)
            else:
                raise ProtocolError(
                    "Admin information can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for admin info from a non-existent user"
            )
    
    def request_serverinfo(self, origin, target):
        """
        Handle requests for server info
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTINFO, origin, target)
            else:
                raise ProtocolError(
                    "Server information can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for server info from a non-existent user"
            )
    
    def request_lusers(self, origin, target, dummy):
        """
        Handle requests for local user info
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTLUSERS,
                               origin, target, dummy)
            else:
                raise ProtocolError(
                    "Luser information can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for Luser info from a non-existent user"
            )
    
    def request_links(self, origin, target, mask):
        """
        Handle requests for links info
        
        Mask can specify a mask of which servers to obtain information on
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTLINKS,
                               origin, target, mask)
            else:
                raise ProtocolError(
                    "Links information can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for links info from a non-existent user"
            )
    
    def request_motd(self, origin, target):
        """
        Request the message of the day for the target server
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTMOTD, origin, target)
            else:
                raise ProtocolError(
                    "MOTD can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for MOTD from a non-existent user"
            )
    
    def request_version(self, origin, target):
        """
        Request version of the target server
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTVERSION, origin, target)
            else:
                raise ProtocolError(
                    "Version can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for version from a non-existent user"
            )
    
    def request_stats(self, origin, target, stat, arg):
        """
        Request some stats from a target server. The stat is the statistic to
        request, and arg is an optional argument for some forms of stats
        requests
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTSTATS,
                               origin, target, stat, arg)
            else:
                raise ProtocolError(
                    "Stats can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for stats from a non-existent user"
            )
    
    def trace(self, origin, search, target):
        """
        Trace a path to the target
        """
        
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_TRACE, origin, search, target)
            else:
                raise ProtocolError(
                    "Traces can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for a trace from a non-existent user"
            )
    
    @property
    def ts(self):
        """
        Returns our current timestamp
        """
        return int(time.time())
    
    #
    # Callbacks
    #
    
    # Constants for Callbacks
    CALLBACK_NEWUSER = "NewUser"
    CALLBACK_QUIT = "Quit"
    CALLBACK_KILL = "Kill"
    CALLBACK_USERMODECHANGE = "UserModeChange"
    CALLBACK_CHANGENICK = "ChangeNick"
    CALLBACK_NEWSERVER = "NewServer"
    CALLBACK_SERVERQUIT = "Squit"
    CALLBACK_AUTHENTICATE = "Authenticate"
    CALLBACK_AWAY = "Away"
    CALLBACK_BACK = "Back"
    CALLBACK_SILENCEADD = "SilenceAdd"
    CALLBACK_SILENCEREMOVE = "SilenceRemove"
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
    CALLBACK_CHANNELTOPIC = "ChannelTopic"
    CALLBACK_GLINEADD = "GlineAdd"
    CALLBACK_GLINEREMOVE = "GlineRemove"
    CALLBACK_INVITE = "Invite"
    CALLBACK_JUPEADD = "JupeAdd"
    CALLBACK_JUPEREMOVE = "JupeRemove"
    CALLBACK_REQUESTADMIN = "RequestAdmin"
    CALLBACK_REQUESTINFO = "RequestInfo"
    CALLBACK_REQUESTLUSERS = "RequestLusers"
    CALLBACK_REQUESTLINKS = "RequestLinks"
    CALLBACK_REQUESTMOTD = "RequestMOTD"
    CALLBACK_REQUESTNAMES = "RequestNames"
    CALLBACK_REQUESTVERSION = "RequestVersion"
    CALLBACK_REQUESTSTATS = "RequestStats"
    CALLBACK_TRACE = "Trace"
    CALLBACK_PING = "Ping"
    CALLBACK_PONG = "Pong"
    CALLBACK_REQUESTWHOIS = "Whois"
    CALLBACK_PRIVMSG = "Privmsg"
    CALLBACK_OOBMSG = "Oobmsg"
    CALLBACK_NOTICE = "Notice"
    CALLBACK_WALLOPS = "Wallops"
    CALLBACK_WALLUSERS = "Wallusers"
    CALLBACK_WALLVOICES = "Wallvoices"
    CALLBACK_WALLCHOPS = "Wallchops"
    
    def register_callback(self, callback, callbackfn):
        self._callbacks[callback].append(callbackfn)
    
    def deregister_callback(self, callback, callbackfn):
        if callbackfn in self._callbacks[callback]:
            self._callbacks[callback].remove(callbackfn)
    
    def _callback(self, callback, *args):
        for callback in self._callbacks.get(callback, []):
            callback(*args)
    
    #
    # Other servers
    #
    
    def server_exists(self, numeric):
        return numeric in self.servers
    
    def new_server(self, origin, numeric, name, maxclient, boot_ts, link_ts,
                   protocol, hops, flags, description):
        """
        Add a new server
        """
        
        # TODO: More stringent checks - do we have a name clash?
        if self.server_exists(numeric):
            raise StateError("Attempted to add a duplicate server")
        elif origin[1] != None:
            raise ProtocolError("User attempted to add a server")
        else:
            uplink = origin[0]
            if self.server_exists(uplink):
                self.servers[numeric] = Server(
                    uplink, numeric, name, maxclient, boot_ts, link_ts,
                    protocol, hops, flags, description
                )
                self.max_client_numerics[numeric] = maxclient
                self.servers[uplink].add_child(numeric)
            else:
                raise StateError("Unknown server introduced a new server")
        self._callback(self.CALLBACK_NEWSERVER, origin, numeric, name,
                       maxclient, boot_ts, link_ts, protocol, hops, flags,
                       description)
    
    def _get_all_children_of(self, numeric):
        """
        Returns all children of a specific server
        """
        ret = self.servers[numeric].children
        for child in self.servers[numeric].children:
            ret = ret | self._get_all_children_of(child)
        return ret
    
    def quit_server(self, origin, numeric, reason, ts):
        """
        A server splits from the network
        """
        
        callback = False
        if self.server_exists(numeric[0]):
            # Disregard bad TS's
            if ts == 0 or ts == self.servers[numeric[0]].link_ts:
                # Build a set of all servers that will be lost in this split
                serverstogo = self._get_all_children_of(numeric[0])
                serverstogo.add(numeric[0])
                # Quit every user that is on these servers. Channels are
                # automatically cleaned up by quit.
                for user in self.users.copy():
                    if user[0] in serverstogo:
                        self.quit(
                            user,
                            "%s split from the network" % (
                                self.numeric2nick(numeric)
                            ),
                            True)
                self.servers[origin[0]].children.remove(numeric[0])
                for server in serverstogo:
                    del self.servers[server]
                callback = True
        else:
            raise StateError("Server that does not exist was just squitted")
        if callback:
            self._callback(self.CALLBACK_SERVERQUIT,
                           origin, numeric, reason, ts)
    
    def get_next_hop(self, dest):
        """
        Return which direction an entity is from here
        """
        if dest[0] == self.server_id:
            return None
        if dest[0] in self.servers[self.server_id].children:
            return dest[0]
        for server in self.servers[self.server_id].children:
            if dest[0] in self._get_all_children_of(server):
                return server
    
    def register_ping(self, origin, source, target):
        """
        Handle pings received from other servers
        """
        
        if self.server_exists(origin[0]) and origin[1] == None:
            self._callback(self.CALLBACK_PING, origin, source, target)
        else:
            raise StateError("Ping received by non-server")
    
    def register_pong(self, origin, source, target):
        """
        Handle pongs received from other servers
        """
        
        if self.server_exists(origin[0]) and origin[1] == None:
            self._callback(self.CALLBACK_PONG, origin, source, target)
        else:
            raise StateError("Pong received by non-server")
    
    #
    # Jupes
    #
    
    @property
    def jupes(self):
        """
        Returns a list of global jupes
        """
        
        self._cleanup_jupes()
        rj = []
        for jupe in self._jupes:
            if not self._jupes[jupe][4]:
                rj.append(
                    (jupe, self._jupes[jupe][0], self._jupes[jupe][1],
                     self._jupes[jupe][2], self._jupes[jupe][3])
                )
        return rj
    
    def _deactivate_jupe(self, jupe):
        """
        Deactivate a jupe
        """
        self._jupes[jupe] = (self._jupes[jupe][0], self._jupes[jupe][1], False,
                             self._jupes[jupe][3], self._jupes[jupe][4])
    
    def _cleanup_jupes(self):
        """
        Deactivate any jupes which have passed their expiry date
        """
        for jupe in self._jupes.copy():
            if self._jupes[jupe][1] < self.ts:
                self._deactivate_jupe(jupe)
    
    def is_juped(self, server):
        """
        Check whether or not a server is juped
        """
        self._cleanup_jupes()
        if server in self._jupes:
            return self._jupes[server][2]
        else:
            return False
    
    def add_jupe(self, origin, server, target, expire, ts, reason):
        """
        Add a Jupe
        """
        if target == None or target == self.server_id:
            self._jupes[server] = (
                reason, expire, True, ts,target == self.server_id
            )
        self._callback(self.CALLBACK_JUPEADD,
                       origin, server, target, expire, reason)
    
    def remove_jupe(self, origin, server, target, ts):
        """
        Remove a jupe
        """
        if target == None or target == self.server_id:
            if server in self._jupes:
                self._deactivate_jupe(server)
        self._callback(self.CALLBACK_JUPEREMOVE, origin, server, target)
    
    #
    # User handling
    #
    
    def user_exists(self, numeric):
        """
        Check if the user is known to us
        """
        return numeric in self.users
    
    def nick2numeric(self, nick):
        """
        Convert a nick into its relevant numeric
        """
        
        for user in self.users:
            if nick == self.users[user].nickname:
                return user
        
        for server in self.servers:
            if nick == self.servers[server].name:
                return (server, None)
    
    def numeric2nick(self, numeric):
        """
        Get the human-readable nick from the numeric
        """
        
        if self.user_exists(numeric):
            return self.users[numeric].nickname
        elif self.server_exists(numeric[0]) and numeric[1] == None:
            return self.servers[numeric[0]].name
    
    def new_user(self, origin, numeric, nickname, username, hostname, modes, ip,
                 hops, ts, fullname):
        """
        Change state to include a new user
        """
        # TODO: Do we have a name clash?
        if self.server_exists(origin[0]):
            if origin[1] == None:
                if self.user_exists(numeric):
                    raise StateError(
                        "Numeric collision - attempting to create second user" \
                        + "with numeric we already know"
                    )
                else:
                    self.users[numeric] = User(
                        numeric, nickname, username, hostname, modes, ip, hops,
                        ts, fullname
                    )
            else:
                raise ProtocolError("Only servers can create users")
        else:
            raise StateError("A non-existent server tried to create a user")
        self._callback(self.CALLBACK_NEWUSER,
                       origin, numeric, nickname, username, hostname, modes, ip,
                       hops, ts, fullname)
    
    def part_all_channels(self, numeric):
        """
        A user parts all channels
        """
        # Shallow copy to allow us to modify during loop
        for channel in self.users[numeric].channels.copy():
            self.channels[channel].part(numeric)
            self.users[numeric].part(channel)
            self._cleanup_channel(channel)
        self._callback(self.CALLBACK_CHANNELPARTALL, numeric)
    
    def quit(self, numeric, reason, causedbysquit=False):
        """
        A user quits the network
        """
        if self.user_exists(numeric):
            for channel in self.users[numeric].channels:
                self.channels[channel].part(numeric)
                self._cleanup_channel(channel)
            del self.users[numeric]
        else:
            raise StateError("Unknown user tried to quit")
        self._callback(self.CALLBACK_QUIT, numeric, reason, causedbysquit)
    
    def kill(self, origin, target, path, reason):
        """
        A user is forcibly quit from the network
        """
        if target[0] == self.server_id:
            self.quit(target, "Killed (" + reason + ")")
        else:
            self._callback(
                self.CALLBACK_KILL,
                origin, target,
                [self.servers[self.get_next_hop(origin)].name] + path,
                reason
            )
    
    def change_nick(self, origin, numeric, newnick, newts):
        """ Change the nickname of a user on the network """
        # TODO: More stringent checks on new nickname, i.e., is it valid/already
        # in use?
        if self.user_exists(numeric):
            self.users[numeric].nickname = newnick
            self.users[numeric].ts = newts
        else:
            raise StateError('Nick change attempted for unknown user')
        self._callback(self.CALLBACK_CHANGENICK,
                       origin, numeric, newnick, newts)
    
    def change_user_mode(self, numeric, modes):
        """
        Change the umodes for a user
        """
        if self.user_exists(numeric):
            for mode in modes:
                self.users[numeric].change_mode(mode)
        else:
            raise StateError(
                "Attempted to change mode on a user that does not exist"
            )
        self._callback(self.CALLBACK_USERMODECHANGE, numeric, modes)
    
    def authenticate(self, origin, numeric, acname):
        """ Mark a user as authenticated """
        if origin[1] == None:
            if self.server_exists(origin[0]):
                if self.user_exists(numeric):
                    self.users[numeric].auth(acname)
                else:
                    raise StateError(
                        "Authentication state change received for unknown user"
                    )
            else:
                raise StateError("Authentication from unknown server")
        else:
            raise ProtocolError("Only servers can change state")
        self._callback(self.CALLBACK_AUTHENTICATE, origin, numeric, acname)
    
    def get_account_name(self, numeric):
        """
        Get the account name for a user. Blank if not authenticated.
        """
        return self.users[numeric].account
    
    def set_away(self, numeric, reason):
        """ Mark a user as being away. Reason must be non-empty """
        if reason == "":
            raise StateError("Attempted to set an empty away reason")
        if self.user_exists(numeric):
            self.users[numeric].away_reason = reason
        else:
            raise StateError(
                "Attempted to mark a user as away who does not exist"
            )
        self._callback(self.CALLBACK_AWAY, numeric, reason)
    
    def set_back(self, numeric):
        """
        Mark a user as no longer being away
        """
        
        if self.user_exists(numeric):
            self.users[numeric].away_reason = None
        else:
            raise StateError(
                "Attempted to mark a user as not away who does not exist"
            )
        self._callback(self.CALLBACK_BACK, numeric)
    
    def add_silence(self, numeric, mask):
        """
        Add a mask to a particular user which silences messages from other users
        which match that mask
        """
        if self.user_exists(numeric):
            self.users[numeric].add_silence(mask)
        else:
            raise StateError("Silence added for a user that does not exist")
        self._callback(self.CALLBACK_SILENCEADD, numeric, mask)
    
    def remove_silence(self, numeric, mask):
        """
        Remove a silence mask for a particular user
        """
        if self.user_exists(numeric):
            self.users[numeric].remove_silence(mask)
        else:
            raise StateError("Silence removed from a user that does not exist")
        self._callback(self.CALLBACK_SILENCEREMOVE, numeric, mask)
    
    def request_whois(self, origin, target, search):
        """
        Request information about who is a user
        """
        if self.user_exists(origin):
            if self.server_exists(target[0]) and target[1] == None:
                self._callback(self.CALLBACK_REQUESTWHOIS,
                               origin, target, search)
            else:
                raise StateError("Whois requested from non-server")
        else:
            raise StateError("Whois requested by non-existent user")
    
    #
    # Channel handling
    #
    
    def create_channel(self, origin, name, ts):
        """
        Create a channel. Returns false if the new channel is invalid (i.e., is
        newer than one already known about)
        """
        # TODO: More stringent checks on whether or not this channel can be
        # created (i.e., is badchan'd or juped)
        create_success = False
        callback = False
        if self.user_exists(origin) \
        or (origin[1] == None and self.server_exists(origin[0])):
            # Channel already exists
            if name in self.channels:
                # If our channel is older, disregard.
                # If they're both the same, add new user as op
                if self.channels[name].ts == ts:
                    # If the origin is a server, we have no-one joining a
                    # channel
                    if origin[1] != None:
                        self.join_channel(origin, origin, name, ["o"], ts)
                    create_success = True
                # Their channel is older, overrides ours and merge users
                elif self.channels[name].ts > ts:
                    self.channels[name].ts = ts
                    self.clear_channel_ops(origin, name)
                    self.clear_channel_voices(origin, name)
                    self.clear_channel_bans(origin, name)
                    for mode in self.channels[name].modes:
                        self.change_channel_mode(
                            origin, name, ("-" + mode[0], None)
                        )
                    if origin[1] != None:
                        self.join_channel(origin, origin, name, ["o"], ts)
                    create_success = True
            else:
                self.channels[name] = Channel(name, ts)
                if origin[1] != None:
                    self.channels[name].join(origin, ["o"])
                    self.users[origin].join(name)
                    callback = True
                create_success = True
        else:
            raise StateError("Unknown entity attempted to create a channel")
        if callback:
            self._callback(self.CALLBACK_CHANNELCREATE, origin, name, ts)
        return create_success
    
    def channel_exists(self, name):
        """
        Returns if a channel exists or not
        """
        return name in self.channels
    
    def request_channel_users(self, origin, target, channels):
        """
        Callback for a request for a list of users on a channel (/names)
        """
        if self.user_exists(origin):
            if target[1] == None:
                goodchannels = []
                for channel in channels:
                    # The channel must exist, and the user must be allowed to
                    # view those names so the user can be an oper, or on the
                    # channel, or the channel is not private or secret
                    if self.channel_exists(channel) \
                    and (self.channels[channel].ison(origin) \
                        or self.users[origin].has_mode("o") \
                        or (not self.channels[channel].has_mode("p") \
                            and not self.channels[channel].has_mode("s"))):
                        goodchannels.append(channel)
                if len(goodchannels) > 0:
                    self._callback(self.CALLBACK_REQUESTNAMES,
                                   origin, target, goodchannels)
            else:
                raise ProtocolError(
                    "Names information can only be requested from servers"
                )
        else:
            raise StateError(
                "Received a request for names info from a non-existent user"
            )
    
    def _cleanup_channel(self, name):
        """
        Remove empty channels
        """
        if len(self.channels[name].users) == 0 \
        and len(self.channels[name].zombies) == 0:
            del self.channels[name]
            for user in self.users:
                # Remove any invites that a user may have to this channel
                if self.users[user].is_invited(name):
                    self.users[user].invites.remove(name)
    
    def destroy_channel(self, origin, channel, ts):
        """
        Destroy a channel
        """
        callback = True
        if self.channel_exists(channel):
            if len(self.channels[channel].users) == 0:
                del self.channels[channel]
            else:
                callback = False
        if callback:
            self._callback(self.CALLBACK_CHANNELDESTROY, origin, channel, ts)
    
    def change_channel_mode(self, origin, name, modes):
        """
        Change the modes on a channel. Modes are lists of tuples of the desired
        change and an optional argument, or None
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                for mode in modes:
                    self.channels[name].change_mode(mode)
            else:
                raise StateError(
                    "Attempted to change the modes on a channel that does not" \
                    + " exist"
                )
        else:
            raise StateError(
                "An invalid entity attempted to change a channel mode"
            )
        self._callback(self.CALLBACK_CHANNELMODECHANGE, origin, name, modes)
    
    def add_channel_ban(self, origin, name, mask):
        """
        Adds a ban to the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                self.channels[name].add_ban(mask)
            else:
                raise StateError(
                    "Attempted to add a ban to a channel that does not exist"
                )
        else:
            raise StateError("An invalid entity attempted to add a channel ban")
        self._callback(self.CALLBACK_CHANNELBANADD, origin, name, mask)
    
    def remove_channel_ban(self, origin, name, ban):
        """
        Removes a ban from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                self.channels[name].remove_ban(ban)
            else:
                raise StateError(
                    "Attempted to remove a ban from a channel that does not" \
                    + " exist"
                )
        else:
            raise StateError(
                "An invalid entity attempted to remove a channel ban"
            )
        self._callback(self.CALLBACK_CHANNELBANREMOVE, origin, name, ban)
    
    def clear_channel_bans(self, origin, name):
        """
        Clears all bans from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                self.channels[name].clear_bans()
            else:
                raise StateError(
                    "Attempted to clear bans from a channel that does not exist"
                )
        else:
            raise StateError(
                "An invalid entity attempted to clear channel bans"
            )
        self._callback(self.CALLBACK_CHANNELBANCLEAR, origin, name)
    
    def change_topic(self, origin, channel, topic, topic_ts, channel_ts):
        """
        Change the topic for a channel
        """
        callback = False
        if self.user_exists(origin) or self.server_exists(origin[0]):
            if self.channel_exists(channel):
                # Disregard if new topic_ts is older than old one
                if topic_ts >= self.channels[channel].topic_ts \
                and channel_ts <= self.channels[channel].ts:
                    self.channels[channel].change_topic(
                        topic, topic_ts, self.numeric2nick(origin)
                    )
                    callback = True
            else:
                raise StateError(
                    "Topic change attempted on a channel that does not exist"
                )
        else:
            raise StateError("Invalid origin attempted to change topic")
        if callback:
            self._callback(self.CALLBACK_CHANNELTOPIC,
                           origin, channel, topic, topic_ts, channel_ts)
    
    #
    # User channel events
    #
    
    def join_channel(self, origin, numeric, name, modes, ts=1270080000):
        """
        A user joins a channel, with optional modes already set. If the channel
        does not exist, it is created.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # join this channel
        callback = False
        if self.user_exists(numeric):
            if self.channel_exists(name):
                self.channels[name].join(numeric, modes)
                self.users[numeric].join(name)
                callback = True
            else:
                # Channel doesn't exist, so it gets created
                self.create_channel(numeric, name, ts)
                # But, modes don't get propagated by create, it always assumes o
                # So bounce deop if needed
                if "o" not in modes:
                    self.deop(origin, name, numeric)
                # And send voice if needed
                if "v" in modes:
                    self.voice(origin, name, numeric)
        else:
            raise StateError(
                "Unknown user (%s) attempted to join a channel" % str(numeric)
            )
        if callback:
            self._callback(self.CALLBACK_CHANNELJOIN,
                           origin, numeric, name, modes, ts)
            if "o" in modes:
                self._callback(self.CALLBACK_CHANNELOP, origin, name, numeric)
            if "v" in modes:
                self._callback(self.CALLBACK_CHANNELVOICE,
                               origin, name, numeric)
    
    def part_channel(self, numeric, name, reason):
        """
        A user parts a channel
        """
        callback_zombie = True
        if self.user_exists(numeric):
            if self.channel_exists(name):
                if self.channels[name].ison(numeric):
                    if numeric in self.channels[name].users:
                        callback_zombie = False
                    self.channels[name].part(numeric)
                    self.users[numeric].part(name)
                    self._cleanup_channel(name)
                else:
                    raise StateError(
                        "User that was not on a channel attempted to leave it"
                    )
            else:
                raise StateError(
                    "User tried to leave a channel that does not exist"
                )
        else:
            raise StateError("Unknown user attempted to leave a channel")
        if callback_zombie:
            self._callback(self.CALLBACK_CHANNELPARTZOMBIE, numeric, name)
        else:
            self._callback(self.CALLBACK_CHANNELPART, numeric, name, reason)
    
    def kick(self, origin, channel, target, reason):
        bouncepart = False
        # Kick handling is weird. We zombify the user until we receive an
        # upstream part
        if self.channel_exists(channel):
            if self.channels[channel].ison(target):
                self.channels[channel].kick(target)
                if target[0] == self.server_id:
                    bouncepart = True
                    self.channels[channel].part(target)
                    self.users[target].part(channel)
                    self._cleanup_channel(channel)
            else:
                raise StateError(
                    "Kick received for a user that is not on the channel"
                )
        else:
            raise StateError("Kick received for a user on an unknown channel")
        self._callback(self.CALLBACK_CHANNELKICK,
                       origin, channel, target, reason)
        if bouncepart:
            self._callback(self.CALLBACK_CHANNELPARTZOMBIE, target, channel)
    
    def op(self, origin, channel, user):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(channel):
                if self.channels[channel].ison(user):
                    self.channels[channel].op(user)
                else:
                    raise StateError(
                        "Attempted to op a user that was not on the channel"
                    )
            else:
                raise StateError(
                    "Attempted to op a user on a channel that does not exist"
                )
        self._callback(self.CALLBACK_CHANNELOP, origin, channel, user)
    
    def deop(self, origin, channel, user):
        """
        Deops a user from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(channel):
                if self.channels[channel].isop(user):
                    self.channels[channel].deop(user)
                else:
                    raise StateError(
                       'Attempted to deop a user that was not op on the channel'
                    )
            else:
                raise StateError(
                    'Attempted to deop from a channel that does not exist'
                )
        else:
            raise StateError("An invalid entity attempted to deop a user")
        self._callback(self.CALLBACK_CHANNELDEOP, origin, channel, user)
    
    def clear_channel_ops(self, origin, name):
        """
        Clears all ops from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                self.channels[name].clear_ops()
            else:
                raise StateError(
                    "Attempted to clear ops from a channel that does not exist"
                )
        else:
            raise StateError("An invalid entity attempted to clear channel ops")
        self._callback(self.CALLBACK_CHANNELCLEAROPS, origin, name)
    
    def voice(self, origin, channel, user):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(channel):
                if self.channels[channel].ison(user):
                    self.channels[channel].voice(user)
                else:
                    raise StateError(
                        "Attempted to voice a user that was not on the channel"
                    )
            else:
                raise StateError(
                    "Attempted to voice a user on a channel that does not exist"
                )
        self._callback(self.CALLBACK_CHANNELVOICE, origin, channel, user)
    
    def devoice(self, origin, channel, user):
        """
        Devoices a user from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(channel):
                if self.channels[channel].isvoice(user):
                    self.channels[channel].devoice(user)
                else:
                    raise StateError(
                        'Attempted to devoice a user that was not voice ' \
                        + 'on the channel'
                    )
            else:
                raise StateError(
                    'Attempted to devoice from a channel that does not exist'
                )
        else:
            raise StateError("An invalid entity attempted to devoice a user")
        self._callback(self.CALLBACK_CHANNELDEVOICE, origin, channel, user)
    
    def clear_channel_voices(self, origin, name):
        """
        Clears all voices from the channel.
        """
        # TODO: More stringent checks on whether or not this user is allowed to
        # make this mode change
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            if self.channel_exists(name):
                self.channels[name].clear_voices()
            else:
                raise StateError(
                    "Attempted to clear voices from a channel that does " \
                    + "not exist"
                )
        else:
            raise StateError(
                "An invalid entity attempted to clear channel voices"
            )
        self._callback(self.CALLBACK_CHANNELCLEARVOICES, origin, name)
    
    def invite(self, origin, target, channel):
        """
        Origin invites Target to Channel
        """
        # TODO: Check origin can actually send invites
        if self.user_exists(target):
            if self.channel_exists(channel):
                self.users[target].invite(channel)
            else:
                raise StateError(
                    "Attempted to invite a user into a non-existent channel"
                )
        else:
            raise StateError(
                "Attempted to invite a non-existent user to a channel"
            )
        self._callback(self.CALLBACK_INVITE, origin, target, channel)
    
    #
    # Messages
    #
    
    def oobmsg(self, origin, target, type, args):
        """
        An out-of-band message
        """
        self._callback(self.CALLBACK_OOBMSG, (origin, target, type, args))
    
    def privmsg(self, origin, target, message):
        """
        A 'private' message (destination can be a channel, which means it's
        shared with an entire channel)
        """
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_PRIVMSG, origin, target, message)
        else:
            raise StateError("Privmsg received from non-existent entity")
    
    def notice(self, origin, target, message):
        """
        A notice message (destination can be a channel, which means it's
        shared with an entire channel)
        """
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_NOTICE, origin, target, message)
        else:
            raise StateError("Notice received from non-existent entity")
    
    def wallops(self, origin, message):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_WALLOPS, origin, message)
        else:
            raise StateError("Wallops received from non-existent entity")
    
    def wallusers(self, origin, message):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_WALLUSERS, origin, message)
        else:
            raise StateError("Wallusers received from non-existent entity")
    
    def wallvoices(self, origin, channel, message):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_WALLVOICES, origin, channel, message)
        else:
            raise StateError("Wallvoices received from non-existent entity")
    
    def wallchops(self, origin, channel, message):
        if self.user_exists(origin) \
        or (self.server_exists(origin[0]) and origin[1] == None):
            self._callback(self.CALLBACK_WALLCHOPS, origin, channel, message)
        else:
            raise StateError("Wallchops received from non-existent entity")
    
    #
    # G-lines
    #
    
    @property
    def glines(self):
        """
        Returns a list of global g-lines
        [(mask, description, expires, active, last modified time)]
        """
        
        self._cleanup_glines()
        rg = []
        for gline in self._glines:
            if not self._glines[gline][4]:
                rg.append(
                    (gline, self._glines[gline][0], self._glines[gline][1],
                     self._glines[gline][2], self._glines[gline][3])
                )
        return rg
    
    def _cleanup_glines(self):
        """
        Remove expired g-lines
        """
        # Make shallow copy of dictionary so we can modify it during iteration
        for gline in self._glines.copy():
            # Remove expired g-lines
            if self._glines[gline][1] < self.ts:
                self._deactivate_gline(gline)
    
    def _deactivate_gline(self, gline):
        """
        Deactivate a g-line
        """
        self._glines[gline] = (
            self._glines[gline][0], self._glines[gline][1], False,
            self._glines[gline][3], self._glines[gline][4]
        )
    
    def add_gline(self, origin, mask, target, expires, ts, description):
        """
        Add a g-line
        """
        # TODO: Check if origin can actually set g-lines
        if target == None or target == self.server_id:
            self._glines[mask] = (
                description, expires, True, ts, target == self.server_id
            )
        self._callback(self.CALLBACK_GLINEADD,
                       origin, mask, target, expires,description)
    
    def is_glined(self, host):
        """
        Check if someone is g-lined
        """
        self._cleanup_glines()
        for mask in self._glines:
            if fnmatch.fnmatch(host, mask):
                return self._glines[mask][2]
            else:
                return False
    
    def remove_gline(self, origin, mask, target, ts):
        """
        Remove a g-line
        """
        # TODO: Check if origin can actually remove g-lines
        if target == None or target == self.server_id:
            for gline in self._glines.copy():
                # Remove any g-lines that match that mask
                if fnmatch.fnmatch(gline, mask):
                    self._deactivate_gline(gline)
        self._callback(self.CALLBACK_GLINEREMOVE, origin, mask, target)


class User():
    """
    Represents a user internally
    """
    
    def __init__(self, numeric, nickname, username, hostname, modes, ip, hops,
                 ts, fullname):
        self.numeric = numeric
        self.nickname = nickname
        self.username = username
        self.hostname = hostname
        self.account = ''
        self._modes = dict()
        for mode in modes:
            self.change_mode(mode)
        self.ip = ip
        self.hops = hops
        self.ts = ts
        self.fullname = fullname
        self.away_reason = None
        self.channels = set()
        self.invites = set()
        self.silences = set()
    
    def auth(self, account):
        """
        Mark this user as authenticated
        """
        if self.account == "":
            self.account = account
            self._modes["r"] = account
        else:
            raise StateError(
                "Authentication state change received for someone who is " \
                + "already authenticated"
            )
    
    def change_mode(self, mode):
        """
        Change a single mode associated with this user
        """
        if mode[0][0] == "+" and mode[1] == None:
            self._modes[mode[0][1]] = True
        elif mode[0][0] == "+" and mode[1] != None:
            self._modes[mode[0][1]] = mode[1]
            # If this mode is an authentication mode (i.e., in a burst)
            if mode[0][1] == "r":
                self.auth(mode[1])
        else:
            self._modes[mode[0][1]] = False
    
    def has_mode(self, mode):
        """
        Return whether a user has a mode
        """
        if mode in self._modes:
            return self._modes[mode]
        else:
            return False
    
    @property
    def modes(self):
        """
        Return the modes this user has
        """
        ml = []
        for mode in self._modes:
            if self._modes[mode] == True:
                ml.append(("+" + mode, None))
            elif self._modes[mode] == False:
                pass
            else:
                ml.append(("+" + mode, str(self._modes[mode])))
        return ml
    
    def is_away(self):
        """
        Return whether a user is away or not
        """
        if self.away_reason == None:
            return False
        else:
            return True
    
    def join(self, channel):
        self.channels.add(channel)
        if self.is_invited(channel):
            self.invites.remove(channel)
    
    def part(self, channel):
        self.channels.remove(channel)
    
    def invite(self, channel):
        self.invites.add(channel)
    
    def is_invited(self, channel):
        return channel in self.invites
    
    def add_silence(self, mask):
        self.silences.add(mask)
    
    def remove_silence(self, mask):
        self.silences = self.silences - set([mask])
    
    def is_silenced(self, mask):
        """ Returns whether or not this user has silenced this host """
        for silence in self.silences:
            if fnmatch.fnmatch(mask, silence):
                return True
        return False


class Channel():
    """ Represents a channel internally """
    
    def __init__(self, name, ts):
        self.name = name
        self.ts = ts
        self._users = dict()
        self.zombies = set()
        self._modes = dict()
        self.bans = []
        self.topic = ""
        self.topic_changer = ""
        self.topic_ts = 0
    
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
    
    def change_mode(self, mode):
        """
        Change a single mode associated with this channel
        """
        if mode[0][0] == "+" and mode[1] == None:
            self._modes[mode[0][1]] = True
        elif mode[0][0] == "+" and mode[1] != None:
            self._modes[mode[0][1]] = mode[1]
        else:
            self._modes[mode[0][1]] = False
    
    def has_mode(self, mode):
        """
        Return whether a channel has a mode (and if it's something with an
        option, what it is)
        """
        if mode in self._modes:
            return self._modes[mode]
        else:
            return False
    
    @property
    def modes(self):
        ml = []
        for mode in self._modes:
            if self._modes[mode] == True:
                ml.append(("+" + mode, None))
            elif self._modes[mode] == False:
                pass
            else:
                ml.append(("+" + mode, str(self._modes[mode])))
        return ml
    
    def clear_bans(self):
        """
        Clears bans from the channel
        """
        self.bans = []
    
    def add_ban(self, mask):
        """
        Adds a ban to the channel
        """
        self.bans.append(mask)
    
    def remove_ban(self, mask):
        """
        Removes a ban from the channel
        """
        for ban in self.bans:
            if fnmatch.fnmatch(ban, mask):
                self.bans.remove(ban)
    
    def ison(self, numeric):
        """
        Returns whether a not a user is on a channel
        """
        return numeric in self._users
    
    @property
    def users(self):
        """
        Return the list of users
        """
        r = self._users.copy()
        for z in self.zombies:
            del r[z]
        return r
    
    def isop(self, numeric):
        """
        Check if a user is op on a channel
        """
        if self.ison(numeric):
            return "o" in self._users[numeric]
        else:
            return False
    
    @property
    def ops(self):
        ret = set()
        for user in self.users:
            if self.isop(user):
                ret.add(user)
        return ret
    
    def op(self, numeric):
        self._users[numeric].add("o")
    
    def deop(self, numeric):
        self._users[numeric].remove("o")
    
    def clear_ops(self):
        for op in self.ops:
            self.deop(op)
    
    def isvoice(self, numeric):
        """
        Check if a user is voice on a channel
        """
        if self.ison(numeric):
            return "v" in self._users[numeric]
        else:
            return False
    
    @property
    def voices(self):
        ret = set()
        for user in self.users:
            if self.isvoice(user):
                ret.add(user)
        return ret
    
    def voice(self, numeric):
        self._users[numeric].add("v")
    
    def devoice(self, numeric):
        self._users[numeric].remove("v")
    
    def clear_voices(self):
        for voice in self.voices:
            self.devoice(voice)
    
    def change_topic(self, new_topic, ts, name):
        self.topic = new_topic
        self.topic_ts = ts
        self.topic_changer = name


class Server():
    """
    Internally represent a server
    """
    
    def __init__(self, origin, numeric, name, maxclient, boot_ts, link_ts,
                 protocol, hops, flags, description):
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
    
    def add_child(self, child):
        self.children.add(child)


class StateError(Exception):
    """
    An exception raised if a state change would be impossible, generally
    suggesting we've gone out of sync
    """
    pass
