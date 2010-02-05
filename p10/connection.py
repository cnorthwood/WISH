#!/usr/bin/env python

# Things that aren't implemented:
# * RPING
# * RPONG
# * ASLL
# * UPING
# * WHOWAS

#import threading
import asyncore
import socket
import fnmatch

import base64
import parser
import commands.account
import commands.admin
import commands.asll
import commands.away
import commands.burst
import commands.clearmode
import commands.connect
import commands.create
import commands.destruct
import commands.end_of_burst
import commands.eob_ack
import commands.error
import commands.gline
import commands.info
import commands.invite
import commands.join
import commands.jupe
import commands.kick
import commands.kill
import commands.links
import commands.lusers
import commands.mode
import commands.motd
import commands.names
import commands.nick
import commands.notice
import commands.numberrelay
import commands.part
import commands.password
import commands.ping
import commands.pong
import commands.privmsg
import commands.quit
import commands.rping
import commands.rpong
import commands.server
import commands.settime
import commands.silence
import commands.squit
import commands.stats
import commands.svsjoin
import commands.svsnick
import commands.time
import commands.topic
import commands.trace
import commands.uping
import commands.version
import commands.wallchops
import commands.wallops
import commands.wallusers
import commands.wallvoices
import commands.whois
import commands.whowas

class connection(asyncore.dispatcher):
    """ Represents a connection upstream """
    
    _state = None
    connstate = None
    _parser = None
    numeric = None
    _endpoint = None
    _password = None
    _upstream_password = None
    _buffer = ""
    _data = ""
    _last_pong = 0
    
    DISCONNECTED = 0
    CONNECTED = 1
    CHALLENGED = 2
    HANDSHAKE = 3
    AUTHENTICATED = 4
    COMPLETE = 5
    
    def __init__(self, state):
        """ Sets up the state that this connection will alter """
        asyncore.dispatcher.__init__(self)
        self._state = state
        self.connstate = self.DISCONNECTED
        self.numeric = None
        self._upstream_password = None
        self._password = None
        self._endpoint = None
        self._parser =  parser.parser(state.maxClientNumerics)
        self._buffer = ""
        self._data = ""
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self, endpoint, password):
        # Create our socket
        self._endpoint = endpoint
        self._password = password
        self._connect()
        return self
    
    def _connect(self):
        self.connect(self._endpoint)
        self.connstate = self.CONNECTED

        # Send pass and server - don't use the parser at this point
        self._buffer += "PASS :" + self._password + "\r\n"
        self._buffer += "SERVER " + self._state.getServerName() + " 1 " + str(self._state.ts()) + " " + str(self._state.ts()) + " J10 " + base64.createNumeric((self._state.getServerID(), 262143)) + " +s :" + self._state.getServerDescription() + "\r\n"
        self.connstate = self.CHALLENGED
        
        # Set up stuff for authentication
        self._parser.registerHandler("PASS", commands.password.password(self._state, self))
        self._parser.registerHandler("ERROR", commands.error.error(self._state))
        self._last_pong = self._state.ts()
        self._last_ping = self._state.ts()
    
    def _setupCallbacks(self):
        self._state.registerCallback(self._state.CALLBACK_NEWUSER, self.callbackNewUser)
        self._state.registerCallback(self._state.CALLBACK_CHANGENICK, self.callbackChangeNick)
        self._state.registerCallback(self._state.CALLBACK_NEWSERVER, self.callbackNewServer)
        self._state.registerCallback(self._state.CALLBACK_AUTHENTICATE, self.callbackAuthenticate)
        self._state.registerCallback(self._state.CALLBACK_USERMODECHANGE, self.callbackChangeUserMode)
        self._state.registerCallback(self._state.CALLBACK_AWAY, self.callbackAway)
        self._state.registerCallback(self._state.CALLBACK_BACK, self.callbackBack)
        self._state.registerCallback(self._state.CALLBACK_CHANNELCREATE, self.callbackChannelCreate)
        self._state.registerCallback(self._state.CALLBACK_CHANNELJOIN, self.callbackChannelJoin)
        self._state.registerCallback(self._state.CALLBACK_CHANNELPART, self.callbackChannelPart)
        self._state.registerCallback(self._state.CALLBACK_CHANNELPARTALL, self.callbackPartAll)
        self._state.registerCallback(self._state.CALLBACK_CHANNELMODECHANGE, self.callbackChannelChangeMode)
        self._state.registerCallback(self._state.CALLBACK_CHANNELBANADD, self.callbackChannelAddBan)
        self._state.registerCallback(self._state.CALLBACK_CHANNELBANREMOVE, self.callbackChannelRemoveBan)
        self._state.registerCallback(self._state.CALLBACK_CHANNELBANCLEAR, self.callbackChannelClearBans)
        self._state.registerCallback(self._state.CALLBACK_CHANNELOP, self.callbackChannelOp)
        self._state.registerCallback(self._state.CALLBACK_CHANNELDEOP, self.callbackChannelDeop)
        self._state.registerCallback(self._state.CALLBACK_CHANNELCLEAROPS, self.callbackChannelClearOps)
        self._state.registerCallback(self._state.CALLBACK_CHANNELVOICE, self.callbackChannelVoice)
        self._state.registerCallback(self._state.CALLBACK_CHANNELDEVOICE, self.callbackChannelDevoice)
        self._state.registerCallback(self._state.CALLBACK_CHANNELCLEARVOICES, self.callbackChannelClearVoices)
        self._state.registerCallback(self._state.CALLBACK_GLINEADD, self.callbackGlineAdd)
        self._state.registerCallback(self._state.CALLBACK_GLINEREMOVE, self.callbackGlineRemove)
        self._state.registerCallback(self._state.CALLBACK_INVITE, self.callbackInvite)
        self._state.registerCallback(self._state.CALLBACK_JUPEADD, self.callbackJupeAdd)
        self._state.registerCallback(self._state.CALLBACK_JUPEREMOVE, self.callbackJupeRemove)
        self._state.registerCallback(self._state.CALLBACK_REQUESTADMIN, self.callbackAdminInfo)
        self._state.registerCallback(self._state.CALLBACK_REQUESTINFO, self.callbackInfoRequest)
        self._state.registerCallback(self._state.CALLBACK_CHANNELKICK, self.callbackKick)
        self._state.registerCallback(self._state.CALLBACK_CHANNELPARTZOMBIE, self.callbackZombiePart)
        self._state.registerCallback(self._state.CALLBACK_CHANNELDESTROY, self.callbackChannelDestroy)
        self._state.registerCallback(self._state.CALLBACK_QUIT, self.callbackQuit)
        self._state.registerCallback(self._state.CALLBACK_KILL, self.callbackKill)
        self._state.registerCallback(self._state.CALLBACK_REQUESTLUSERS, self.callbackLusers)
        self._state.registerCallback(self._state.CALLBACK_REQUESTLINKS, self.callbackLinks)
        self._state.registerCallback(self._state.CALLBACK_REQUESTMOTD, self.callbackMOTD)
        self._state.registerCallback(self._state.CALLBACK_REQUESTNAMES, self.callbackNames)
        self._state.registerCallback(self._state.CALLBACK_CHANNELTOPIC, self.callbackTopic)
        self._state.registerCallback(self._state.CALLBACK_SILENCEADD, self.callbackSilenceAdd)
        self._state.registerCallback(self._state.CALLBACK_SILENCEREMOVE, self.callbackSilenceRemove)
        self._state.registerCallback(self._state.CALLBACK_SERVERQUIT, self.callbackSquit)
        self._state.registerCallback(self._state.CALLBACK_REQUESTVERSION, self.callbackRequestVersion)
        self._state.registerCallback(self._state.CALLBACK_REQUESTSTATS, self.callbackRequestStats)
        self._state.registerCallback(self._state.CALLBACK_TRACE, self.callbackTrace)
        self._state.registerCallback(self._state.CALLBACK_PING, self.callbackPing)
        self._state.registerCallback(self._state.CALLBACK_PONG, self.callbackPong)
        self._state.registerCallback(self._state.CALLBACK_REQUESTWHOIS, self.callbackRequestWhois)
        self._state.registerCallback(self._state.CALLBACK_PRIVMSG, self.callbackPrivmsg)
        self._state.registerCallback(self._state.CALLBACK_OOBMSG, self.callbackOobmsg)
        self._state.registerCallback(self._state.CALLBACK_NOTICE, self.callbackNotice)
        self._state.registerCallback(self._state.CALLBACK_WALLOPS, self.callbackWallops)
        self._state.registerCallback(self._state.CALLBACK_WALLUSERS, self.callbackWallusers)
        self._state.registerCallback(self._state.CALLBACK_WALLVOICES, self.callbackWallvoices)
        self._state.registerCallback(self._state.CALLBACK_WALLCHOPS, self.callbackWallchops)
    
    def _teardownCallbacks(self):
        self._state.deregisterCallback(self._state.CALLBACK_NEWUSER, self.callbackNewUser)
        self._state.deregisterCallback(self._state.CALLBACK_CHANGENICK, self.callbackChangeNick)
        self._state.deregisterCallback(self._state.CALLBACK_NEWSERVER, self.callbackNewServer)
        self._state.deregisterCallback(self._state.CALLBACK_AUTHENTICATE, self.callbackAuthenticate)
        self._state.deregisterCallback(self._state.CALLBACK_USERMODECHANGE, self.callbackChangeUserMode)
        self._state.deregisterCallback(self._state.CALLBACK_AWAY, self.callbackAway)
        self._state.deregisterCallback(self._state.CALLBACK_BACK, self.callbackBack)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELCREATE, self.callbackChannelCreate)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELJOIN, self.callbackChannelJoin)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELPART, self.callbackChannelPart)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELPARTALL, self.callbackPartAll)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELMODECHANGE, self.callbackChannelChangeMode)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELBANADD, self.callbackChannelAddBan)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELBANREMOVE, self.callbackChannelRemoveBan)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELBANCLEAR, self.callbackChannelClearBans)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELOP, self.callbackChannelOp)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELDEOP, self.callbackChannelDeop)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELCLEAROPS, self.callbackChannelClearOps)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELVOICE, self.callbackChannelVoice)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELDEVOICE, self.callbackChannelDevoice)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELCLEARVOICES, self.callbackChannelClearVoices)
        self._state.deregisterCallback(self._state.CALLBACK_GLINEADD, self.callbackGlineAdd)
        self._state.deregisterCallback(self._state.CALLBACK_GLINEREMOVE, self.callbackGlineRemove)
        self._state.deregisterCallback(self._state.CALLBACK_INVITE, self.callbackInvite)
        self._state.deregisterCallback(self._state.CALLBACK_JUPEADD, self.callbackJupeAdd)
        self._state.deregisterCallback(self._state.CALLBACK_JUPEREMOVE, self.callbackJupeRemove)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTADMIN, self.callbackAdminInfo)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTINFO, self.callbackInfoRequest)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELKICK, self.callbackKick)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELPARTZOMBIE, self.callbackZombiePart)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELDESTROY, self.callbackChannelDestroy)
        self._state.deregisterCallback(self._state.CALLBACK_QUIT, self.callbackQuit)
        self._state.deregisterCallback(self._state.CALLBACK_KILL, self.callbackKill)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTLUSERS, self.callbackLusers)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTLINKS, self.callbackLinks)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTMOTD, self.callbackMOTD)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTNAMES, self.callbackNames)
        self._state.deregisterCallback(self._state.CALLBACK_CHANNELTOPIC, self.callbackTopic)
        self._state.deregisterCallback(self._state.CALLBACK_SILENCEADD, self.callbackSilenceAdd)
        self._state.deregisterCallback(self._state.CALLBACK_SILENCEREMOVE, self.callbackSilenceRemove)
        self._state.deregisterCallback(self._state.CALLBACK_SERVERQUIT, self.callbackSquit)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTVERSION, self.callbackRequestVersion)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTSTATS, self.callbackRequestStats)
        self._state.deregisterCallback(self._state.CALLBACK_TRACE, self.callbackTrace)
        self._state.deregisterCallback(self._state.CALLBACK_PING, self.callbackPing)
        self._state.deregisterCallback(self._state.CALLBACK_PONG, self.callbackPong)
        self._state.deregisterCallback(self._state.CALLBACK_REQUESTWHOIS, self.callbackRequestWhois)
        self._state.deregisterCallback(self._state.CALLBACK_PRIVMSG, self.callbackPrivmsg)
        self._state.deregisterCallback(self._state.CALLBACK_OOBMSG, self.callbackOobmsg)
        self._state.deregisterCallback(self._state.CALLBACK_NOTICE, self.callbackNotice)
        self._state.deregisterCallback(self._state.CALLBACK_WALLOPS, self.callbackWallops)
        self._state.deregisterCallback(self._state.CALLBACK_WALLUSERS, self.callbackWallusers)
        self._state.deregisterCallback(self._state.CALLBACK_WALLVOICES, self.callbackWallvoices)
        self._state.deregisterCallback(self._state.CALLBACK_WALLCHOPS, self.callbackWallchops)
    
    def _setupParser(self):
        p = self._parser
        p.registerHandler("AC", commands.account.account(self._state))
        p.registerHandler("AD", commands.admin.admin(self._state))
        p.registerHandler("LL", commands.asll.asll(self._state))
        p.registerHandler("A", commands.away.away(self._state))
        p.registerHandler("B", commands.burst.burst(self._state))
        p.registerHandler("CM", commands.clearmode.clearmode(self._state))
        p.registerHandler("CO", commands.connect.connect(self._state))
        p.registerHandler("C", commands.create.create(self._state))
        p.registerHandler("DE", commands.destruct.destruct(self._state))
        p.registerHandler("DS", commands.wallops.wallops(self._state))
        p.registerHandler("EB", commands.end_of_burst.end_of_burst(self._state, self))
        p.registerHandler("EA", commands.eob_ack.eob_ack(self._state))
        p.registerHandler("Y", commands.error.error(self._state))
        p.registerHandler("GL", commands.gline.gline(self._state))
        p.registerHandler("F", commands.info.info(self._state))
        p.registerHandler("I", commands.invite.invite(self._state))
        p.registerHandler("J", commands.join.join(self._state))
        p.registerHandler("JU", commands.jupe.jupe(self._state))
        p.registerHandler("K", commands.kick.kick(self._state))
        p.registerHandler("D", commands.kill.kill(self._state))
        p.registerHandler("LI", commands.links.links(self._state))
        p.registerHandler("LU", commands.lusers.lusers(self._state))
        p.registerHandler("M", commands.mode.mode(self._state))
        p.registerHandler("MO", commands.motd.motd(self._state))
        p.registerHandler("E", commands.names.names(self._state))
        p.registerHandler("N", commands.nick.nick(self._state))
        p.registerHandler("O", commands.notice.notice(self._state))
        p.registerHandler("OM", commands.mode.mode(self._state)) # opmodes get handled exactly the same as normal modes
        p.registerHandler("L", commands.part.part(self._state))
        p.registerHandler("G", commands.ping.ping(self._state, self))
        p.registerHandler("Z", commands.pong.pong(self._state, self))
        p.registerHandler("P", commands.privmsg.privmsg(self._state))
        p.registerHandler("Q", commands.quit.quit(self._state))
        #p.registerHandler("RI", commands.rping.rping(self._state))
        #p.registerHandler("RO", commands.rpong.rpong(self._state))
        p.registerHandler("S", commands.server.server(self._state, None))
        p.registerHandler("SE", commands.settime.settime(self._state))
        p.registerHandler("U", commands.silence.silence(self._state))
        p.registerHandler("SQ", commands.squit.squit(self._state))
        p.registerHandler("R", commands.stats.stats(self._state))
        p.registerHandler("SJ", commands.svsjoin.svsjoin(self._state))
        p.registerHandler("SN", commands.svsnick.svsnick(self._state))
        p.registerHandler("TI", commands.time.time(self._state))
        p.registerHandler("T", commands.topic.topic(self._state))
        p.registerHandler("TR", commands.trace.trace(self._state))
        p.registerHandler("UP", commands.uping.uping(self._state))
        p.registerHandler("V", commands.version.version(self._state))
        p.registerHandler("WC", commands.wallchops.wallchops(self._state))
        p.registerHandler("WA", commands.wallops.wallops(self._state))
        p.registerHandler("WU", commands.wallusers.wallusers(self._state))
        p.registerHandler("WV", commands.wallvoices.wallvoices(self._state))
        p.registerHandler("W", commands.whois.whois(self._state))
        p.registerHandler("X", commands.whowas.whowas(self._state))
        p.registerHandler("252", commands.numberrelay.numberrelay(self._state, "252"))
        p.registerHandler("254", commands.numberrelay.numberrelay(self._state, "254"))
        p.registerHandler("255", commands.numberrelay.numberrelay(self._state, "255"))
        p.registerHandler("256", commands.numberrelay.numberrelay(self._state, "256"))
        p.registerHandler("257", commands.numberrelay.numberrelay(self._state, "257"))
        p.registerHandler("258", commands.numberrelay.numberrelay(self._state, "258"))
        p.registerHandler("259", commands.numberrelay.numberrelay(self._state, "259"))
        p.registerHandler("351", commands.numberrelay.numberrelay(self._state, "351"))
        p.registerHandler("353", commands.numberrelay.numberrelay(self._state, "353"))
        p.registerHandler("364", commands.numberrelay.numberrelay(self._state, "364"))
        p.registerHandler("365", commands.numberrelay.numberrelay(self._state, "365"))
        p.registerHandler("366", commands.numberrelay.numberrelay(self._state, "366"))
        p.registerHandler("371", commands.numberrelay.numberrelay(self._state, "371"))
        p.registerHandler("374", commands.numberrelay.numberrelay(self._state, "374"))
        p.registerHandler("375", commands.numberrelay.numberrelay(self._state, "375"))
        p.registerHandler("376", commands.numberrelay.numberrelay(self._state, "376"))
    
    def _sendLine(self, source_client, token, args):
        """ Send a line upsteam
        
            source_client: An integer, or None, representing which client is sending this message
            token: The token to be sent.
            args: An array of strings making up the message body """
        self._buffer += self._parser.build(source_client, token, args)
    
    def registerNumeric(self, numeric):
        self.numeric = numeric
    
    def registerUpstreamPassword(self, password):
        self._upstream_password = password
    
    def registerEOB(self):
        self._sendLine((self._state.getServerID(), None), "EA", [])
    
    def registerPing(self, arg):
        self._sendLine((self._state.getServerID(), None), "Z", [base64.createNumeric((self._state.getServerID(), None)), arg])
    
    def registerPong(self):
        self._last_pong = self._state.ts()
    
    def close_connection(self):
        self.close()
        self.connstate = self.COMPLETE
    
    def do_ping(self):
        # Give a 60 second grace between ping being sent and timing out
        if (self._state.ts() - 60) > self._last_ping and self._last_ping > self._last_pong:
            self.error("Ping Timeout")
        elif self._last_ping < (self._state.ts() - 180):
            self._sendLine((self._state.getServerID(), None), "G", [base64.createNumeric((self._state.getServerID(), None))])
            self._last_ping = self._state.ts()
    
    def error(self, reason):
        """ TODO: Handles errors on the connection """
        print "ERROR: " + reason
        self._sendLine((self._state.getServerID(), None), "Y", [reason])
    
    def __recursiveBurstServer(self, server):
        # We don't burst ourselves
        if self._state.servers[server].numeric != self._state.getServerID():
            self.callbackNewServer(((self._state.servers[server].origin, None),
                                     self._state.servers[server].numeric,
                                     self._state.servers[server].name,
                                     self._state.servers[server].maxclient,
                                     self._state.servers[server].boot_ts,
                                     self._state.servers[server].link_ts,
                                     self._state.servers[server].protocol,
                                     self._state.servers[server].hops,
                                     self._state.servers[server].flags,
                                     self._state.servers[server].description))
        for child in self._state.servers[server].children:
            # Don't burst the server back to us
            if child != self.numeric:
                self.__recursiveNewServer(child)
    
    def _sendBurst(self):
        # Now we start listening
        self._setupCallbacks()
        
        # Send servers
        self.__recursiveBurstServer(self._state.getServerID())
        
        # Send g-lines
        for (mask, description, expires, active, mod_time) in self._state.glines():
            if active:
                self.callbackGlineAdd(((self._state.getServerID(), None), mask, None, expires, description))
            else:
                self.callbackGlineRemove(((self._state.getServerID(), None), mask, None))
        
        # Send jupes
        for (mask, description, expires, active, mod_time) in self._state.jupes():
            if active:
                self.callbackJupeAdd(((self._state.getServerID(), None), mask, None, expires, description))
            else:
                self.callbackJupeRemove(((self._state.getServerID(), None), mask, None))
        
        # Send users
        for user in self._state.users:
            self.callbackNewUser((  (self._state.users[user].numeric[0], None),
                                    self._state.users[user].numeric,
                                    self._state.users[user].nickname,
                                    self._state.users[user].username,
                                    self._state.users[user].hostname,
                                    self._state.users[user].modes(),
                                    self._state.users[user].ip,
                                    self._state.users[user].hops,
                                    self._state.users[user].ts,
                                    self._state.users[user].fullname))
        
        # Send channels
        for channel in self._state.channels:
            
            # First part of burst
            burst = [channel, str(self._state.channels[channel].ts)]
            
            # Channel modes
            (modestr, modeargs) = self._buildModeString(self._state.channels[channel].modes())
            
            if modestr != "":
                burst.append(modestr)
            burst += modeargs
            
            # Get users on channel
            users = self._state.channels[channel].users()
            ovs = []
            os = []
            vs = []
            plains = []
            for user in users:
                numeric = base64.createNumeric(user)
                if "o" in users[user] and "v" in users[user]:
                    ovs.append(numeric)
                elif "o" in users[user]:
                    os.append(numeric)
                elif "v" in users[user]:
                    vs.append(numeric)
                else:
                    plains.append(numeric)
            
            bans = self._state.channels[channel].bans
            
            done = False
            
            while not done:
                # Limit to 510 in size
                remaining = 510 - 6 # origin and token + spacing
                for arg in burst:
                    remaining -= len(arg)
                    remaining -= 1 # space
                
                userstr = ''
                
                if len(plains) > 0:
                    while len(plains) and remaining > 6:
                        plain = plains.pop()
                        userstr += plain + ","
                        remaining -= len(plain) + 1
                
                if len(vs) > 0:
                    first = True
                    while len(vs) and remaining > 8:
                        v = vs.pop()
                        if first:
                            userstr += v + ":v,"
                            first = False
                        else:
                            userstr += v + ","
                        remaining -= len(v) + 1
                
                if len(os) > 0:
                    first = True
                    while len(os) and remaining > 8:
                        o = os.pop()
                        if first:
                            userstr += o + ":o,"
                            first = False
                        else:
                            userstr += o + ","
                        remaining -= len(o) + 1
                
                if len(ovs) > 0:
                    first = True
                    while len(ovs) and remaining > 9:
                        ov = ovs.pop()
                        if first:
                            userstr += ov + ":ov,"
                            first = False
                        else:
                            userstr += ov + ","
                        remaining -= len(ov) + 1
                
                if userstr != '':
                    burst.append(userstr[:-1])
                
                # Bans
                
                banstr = ''
                
                if len(bans) > 0:
                    first = True
                    while len(bans) and remaining > len(bans[-1]) + 1:
                        ban = bans.pop()
                        if first:
                            banstr += "%" + ban
                            first = False
                        else:
                            banstr += " " + ban
                        remaining -= len(ban) + 1
                
                if banstr != '':
                    burst.append(banstr)
                
                self._sendLine((self._state.getServerID(), None), "B", burst)
                burst = [channel, str(self._state.channels[channel].ts)]
                
                # Check we're done
                if len(plains) == 0 and len(vs) == 0 and len(os) == 0 and len(ovs) == 0 and len(bans) == 0:
                    done = True
        
        self._sendLine((self._state.getServerID(), None), "EB", [])
    
    def writable(self):
        return (len(self._buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self._buffer)
        print "SENT: " + self._buffer[:sent]
        self._buffer = self._buffer[sent:]
    
    def handle_close(self):
        if self.connstate != self.COMPLETE:
            self._state.quitServer((self._state.getServerID(), None), (self.numeric, None), "Connection closed unexpectedly", self._state.ts())
            self.connstate = self.COMPLETE
        self._teardownCallbacks()
        self.close()
    
    def handle_read(self):
        # Get this chunk
        self._data += self.recv(512)

        # Get an entire line
        nlb = self._data.find("\n")
        while nlb > -1:
            line = self._data[:nlb+1]
            print "HANDLING: " + line
            # Update state
            if self.connstate == self.CHALLENGED and self._upstream_password != None:
                # Check password
                if self._password == self._upstream_password:
                    self.connstate = self.HANDSHAKE
                    self._parser.registerHandler("SERVER", commands.server.server(self._state, self))
                else:
                    self.error("Password not as expected")
            if self.connstate == self.HANDSHAKE and self.numeric != None:
                self.connstate = self.AUTHENTICATED
                self._setupParser()
                # We're all good, send netburst
                self._sendBurst()
            if self.connstate < self.AUTHENTICATED:
                try:
                    self._parser.parsePreAuth(line, (self._state.getServerID(), None))
                except Exception, e:
                    self.error(str(e))
            else:
                try:
                    self._parser.parse(line)
                except Exception, e:
                    self.error(str(e))
            # Get our next complete line if one exists
            self._data = self._data[nlb+1:]
            nlb = self._data.find("\n")
        self.do_ping()
    
    def _buildModeString(self, modes):
        modestr = ""
        curmode = ""
        modeargs = []
        for mode in modes:
            if curmode != mode[0][0]:
                modestr += mode[0]
                curmode = mode[0][0]
            else:
                modestr += mode[0][1]
            if mode[1] != None:
                modeargs.append(str(mode[1]))
        return (modestr, modeargs)
    
    def callbackNewUser(self, (origin, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname)):
        # Broadcast to all away from origin
        if self._state.getNextHop(origin) != self.numeric:
            line = [nickname, str(hops + 1), str(ts), username, hostname]
            (modestr, modeargs) = self._buildModeString(modes)
            if modestr != "":
                line.append(modestr)
            line += modeargs
            line.append(base64.toBase64(ip, 6))
            line.append(base64.createNumeric(numeric))
            line.append(fullname)
            self._sendLine(origin, "N", line)
    
    def callbackChangeNick(self, (origin, numeric, newnick, newts)):
        # Broadcast to all away from origin
        if self._state.getNextHop(origin) != self.numeric:
            if origin != numeric:
                self._sendLine(origin, "SN", [base64.createNumeric(numeric), newnick])
            else:
                self._sendLine(numeric, "N", [newnick, str(newts)])
    
    def callbackNewServer(self, (origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description)):
        # Broadcast to all away from origin
        if self._state.getNextHop(origin) != self.numeric:
            (modestr, modeargs) = self._buildModeString(flags)
            if modestr == '':
                modestr = '+'
            self._sendLine(origin, "S", [name, str(hops + 1), str(boot_ts), str(link_ts), protocol, base64.createNumeric((numeric, maxclient)), modestr, description])
    
    def callbackSquit(self, (origin, numeric, reason, ts)):
        # If this uplink is the one being disconnected
        if numeric[0] == self.numeric:
            self.close_connection()
            self._sendLine(origin, "SQ", [self._state.getServerName(), "0", reason])
        # Otherwise, broadcast away from origin
        elif self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "SQ", [self._state.numeric2nick(numeric), str(ts), reason])
    
    def callbackAuthenticate(self, (origin, numeric, acname)):
        # Broadcast to all away from origin
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "AC", [base64.createNumeric(numeric), acname])
    
    def callbackAway(self, (numeric, reason)):
        # Broadcast to all away from origin
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "A", [reason])
    
    def callbackBack(self, (numeric)):
        # Broadcast to all away from origin
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "A", [])
    
    def callbackChannelCreate(self, (origin, name, ts)):
        # Broadcast to all servers away from origin
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "C", [name, str(ts)])
    
    def callbackChannelJoin(self, (origin, numeric, name, modes, ts)):
        # Broadcast to all servers away from origin
        if self._state.getNextHop(origin) != self.numeric:
            # If it's a forced join, must be a SJ
            if origin != numeric:
                self._sendLine(origin, "SJ", [base64.createNumeric(numeric), name])
            else:
                self._sendLine(origin, "J", [name, str(ts)])
            # In theory, joins should never be called if the channel already exists
            # so we must force any modes on
            if "o" in modes:
                self.callbackChannelOp((origin, name, numeric))
            if "v" in modes:
                self.callbackChannelVoice((origin, name, numeric))
    
    def callbackChannelPart(self, (numeric, name, reason)):
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "P", [name, reason])
    
    def callbackPartAll(self, (numeric)):
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "J", ["0"])
    
    def callbackChannelChangeMode(self, (origin, name, modes)):
        if self._state.getNextHop(origin) != self.numeric:
            line = [name]
            (modestr, modeargs) = self._buildModeString(modes)
            line.append(modestr)
            line += modeargs
            line.append(str(self._state.channels[name].ts))
            self._sendLine(origin, "M", line)
    
    def callbackChannelAddBan(self, (origin, name, mask)):
        self.callbackChannelChangeMode((origin, name, [("+b", mask)]))
    
    def callbackChannelRemoveBan(self, (origin, name, ban)):
        self.callbackChannelChangeMode((origin, name, [("-b", ban)]))
    
    def callbackChannelClearBans(self, (origin, name)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "CM", [name, "b"])
    
    def callbackChannelOp(self, (origin, channel, user)):
        self.callbackChannelChangeMode((origin, channel, [("+o", base64.createNumeric(user))]))
    
    def callbackChannelDeop(self, (origin, channel, user)):
        self.callbackChannelChangeMode((origin, channel, [("-o", base64.createNumeric(user))]))
    
    def callbackChannelClearOps(self, (origin, name)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "CM", [name, "o"])
    
    def callbackChannelVoice(self, (origin, channel, user)):
        self.callbackChannelChangeMode((origin, channel, [("+v", base64.createNumeric(user))]))
    
    def callbackChannelDevoice(self, (origin, channel, user)):
        self.callbackChannelChangeMode((origin, channel, [("-v", base64.createNumeric(user))]))
    
    def callbackChannelClearVoices(self, (origin, name)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "CM", [name, "v"])
    
    def _getGline(self, mask):
        for gline in self._state.glines():
            if mask == gline[0]:
                return gline
    
    def callbackGlineAdd(self, (origin, mask, target, expires, description)):
        gline = self._getGline(mask)
        if self._state.getNextHop(origin) != self.numeric and target == None:
            self._sendLine(origin, "GL", ["*", "+" + mask, str(expires - gline[4]), str(gline[4]), description])
        elif self._state.getNextHop((target, None)) == self.numeric:
            self._sendLine(origin, "GL", [base64.createNumeric((target, None)), "+" + mask, str(expires - gline[4]), str(gline[4]), description])
    
    def callbackGlineRemove(self, (origin, mask, target)):
        gline = self._getGline(mask)
        if self._state.getNextHop(origin) != self.numeric and target == None:
            self._sendLine(origin, "GL", ["*", "-" + mask, str(gline[2] - gline[4]), str(gline[4]), gline[1]])
        elif self._state.getNextHop((target, None)) == self.numeric:
            self._sendLine(origin, "GL", [base64.createNumeric((target, None)), "-" + mask, str(gline[2] - gline[4]), str(gline[4]), gline[1]])
    
    def callbackInvite(self, (origin, target, channel)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "I", [self._state.numeric2nick(target), channel])
    
    def _getJupe(self, server):
        for jupe in self._state.jupes():
            if server == jupe[0]:
                return jupe
    
    def callbackJupeAdd(self, (origin, server, target, expire, reason)):
        jupe = self._getJupe(server)
        if self._state.getNextHop(origin) != self.numeric and target == None:
            self._sendLine(origin, "JU", ["*", "+" + server, str(expire - jupe[4]), str(jupe[4]), reason])
        elif self._state.getNextHop((target, None)) == self.numeric:
            self._sendLine(origin, "JU", [base64.createNumeric((target, None)), "+" + server, str(expire - jupe[4]), str(jupe[4]), reason])
    
    def callbackJupeRemove(self, (origin, server, target)):
        jupe = self._getJupe(server)
        if self._state.getNextHop(origin) != self.numeric and target == None:
            self._sendLine(origin, "JU", ["*", "-" + server, str(jupe[2] - jupe[4]), str(jupe[4]), jupe[1]])
        elif self._state.getNextHop((target, None)) == self.numeric:
            self._sendLine(origin, "JU", [base64.createNumeric((target, None)), "-" + server, str(jupe[2] - jupe[4]), str(jupe[4]), jupe[1]])
    
    def callbackAdminInfo(self, (origin, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "AD", [base64.createNumeric(target)])
    
    def callbackInfoRequest(self, (origin, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "F", [base64.createNumeric(target)])
    
    def callbackKick(self, (origin, channel, target, reason)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "K", [channel, base64.createNumeric(target), reason])
    
    def callbackZombiePart(self, (origin, channel)):
        self.callbackChannelPart((origin, channel, "Zombie parting channel"))
    
    def callbackChannelDestroy(self, (origin, channel, ts)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "DE", [channel, str(ts)])
    
    def callbackQuit(self, (numeric, reason, causedbysquit)):
        if not causedbysquit and self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "Q", [reason])
    
    def callbackKill(self, (origin, target, path, reason)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "D", [base64.createNumeric(target), "!".join(path) + " (" + reason + ")"])
    
    def callbackLusers(self, (origin, target, dummy)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "LU", [dummy, base64.createNumeric(target)])
    
    def callbackLinks(self, (origin, target, mask)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "LI", [base64.createNumeric(target), mask])
    
    def callbackChangeUserMode(self, (numeric, modes)):
        if self._state.getNextHop(numeric) != self.numeric:
            line = [self._state.numeric2nick(numeric)]
            (modestr, modeargs) = self._buildModeString(modes)
            line.append(modestr)
            line += modeargs
            self._sendLine(numeric, "M", line)
    
    def callbackMOTD(self, (numeric, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(numeric, "MO", [base64.createNumeric(target)])
    
    def callbackNames(self, (origin, target, channels)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "E", [",".join(channels), base64.createNumeric(target)])
    
    def callbackTopic(self, (origin, channel, topic, topic_ts, channel_ts)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "T", [channel, str(channel_ts), str(topic_ts), topic])
    
    def callbackSilenceAdd(self, (numeric, mask)):
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "U", ["*", mask])
    
    def callbackSilenceRemove(self, (numeric, mask)):
        if self._state.getNextHop(numeric) != self.numeric:
            self._sendLine(numeric, "U", ["*", "-" + mask])
    
    def callbackRequestVersion(self, (origin, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "V", [base64.createNumeric(target)])
    
    def callbackRequestStats(self, (origin, target, stat, arg)):
        if self._state.getNextHop(target) == self.numeric:
            if arg != None:
                self._sendLine(origin, "R", [stat, base64.createNumeric(target), arg])
            else:
                self._sendLine(origin, "R", [stat, base64.createNumeric(target)])
    
    def callbackTrace(self, (origin, search, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "TR", [search, base64.createNumeric(target)])
    
    def callbackPing(self, (origin, source, target)):
        if target[0] == self._state.getServerID() and self._state.getNextHop(origin) == self.numeric:
            self._sendLine((self._state.getServerID(), None), "Z", [base64.createNumeric((self._state.getServerID(), None)), source])
        elif self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "G", [source, base64.createNumeric(target)])
    
    def callbackPong(self, (origin, source, target)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "Z", [base64.createNumeric(source), base64.createNumeric(target)])
    
    def callbackRequestWhois(self, (origin, target, search)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, "W", [base64.createNumeric(target), search])
    
    def _multiTargetMessage(self, origin, target, type, message):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, type, [base64.createNumeric(target), message])
        elif target[0] == "#":
            if self._state.getNextHop(origin) != self.numeric:
                for user in self._state.channels[target].users():
                    if self._state.getNextHop(user) == self.numeric:
                        self._sendLine(origin, type, [target, message])
        elif "@" in target:
            target_parts = target.split("@")
            if self._state.getNextHop(self._state.nick2numeric(target_parts[1])) == self.numeric:
                self._sendLine(origin, type, [target, message])
        elif "$" in target:
            mask = target[1:]
            for server in self._state.servers:
                if self._state.getNextHop((server, None)) == self.numeric and fnmatch.fnmatch(self._state.servers[server].name, mask):
                    self._sendLine(origin, type, [target, message])
                    return
    
    def callbackPrivmsg(self, (origin, target, message)):
        self._multiTargetMessage(origin, target, "P", message)
    
    def callbackNotice(self, (origin, target, message)):
        self._multiTargetMessage(origin, target, "O", message)
    
    def callbackOobmsg(self, (origin, target, type, args)):
        if self._state.getNextHop(target) == self.numeric:
            self._sendLine(origin, type, [base64.createNumeric(target)] + args)
    
    def callbackWallops(self, (origin, message)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "WA", [message])
    
    def callbackWallusers(self, (origin, message)):
        if self._state.getNextHop(origin) != self.numeric:
            self._sendLine(origin, "WU", [message])
    
    def callbackWallvoices(self, (origin, channel, message)):
        if self._state.getNextHop(origin) != self.numeric:
            for user in self._state.channels[channel].users():
                if self._state.getNextHop(user) == self.numeric and (self._state.channels[channel].isvoice(user) or self._state.channels[channel].isop(user)):
                    self._sendLine(origin, "WV", [channel, message])
                    return
        
    def callbackWallchops(self, (origin, channel, message)):
        if self._state.getNextHop(origin) != self.numeric:
            for user in self._state.channels[channel].users():
                if self._state.getNextHop(user) == self.numeric and self._state.channels[channel].isop(user):
                    self._sendLine(origin, "WC", [channel, message])
                    return


class ConnectionError(Exception):
    """ When an error occurs in a connection """
    pass
