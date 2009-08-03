#!/usr/bin/env python

import threading
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
import commands.desynch
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
import commands.opmode
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
import commands.who
import commands.whois
import commands.whowas

class connection(threading.Thread):
    """ Represents a connection upstream """
    
    _state = None
    _parser = None
    _socket = None
    
    def __init__(self, state):
        """ Sets up the state that this connection will alter """
        self._state = state
        self._setupParser()
        threading.Thread.__init__(self)
    
    def _setupParser(self):
        p = parser.parser(self._state.maxClientNumerics)
        p.registerHandler("AC", commands.account.account(self._state))
        p.registerHandler("AD", commands.admin.admin(self._state))
        p.registerHandler("LL", commands.asll.asll(self._state))
        p.registerHandler("A", commands.away.away(self._state))
        p.registerHandler("B", commands.burst.burst(self._state))
        p.registerHandler("CM", commands.clearmode.clearmode(self._state))
        p.registerHandler("CO", commands.connect.connect(self._state))
        p.registerHandler("C", commands.create.create(self._state))
        p.registerHandler("DE", commands.destruct.destruct(self._state))
        #p.registerHandler("DS", commands.desynch.desynch(self._state))
        #p.registerHandler("EB", commands.end_of_burst.end_of_burst(self._state))
        #p.registerHandler("EA", commands.eob_ack.eob_ack(self._state))
        p.registerHandler("Y", commands.error.error(self._state))
        p.registerHandler("GL", commands.gline.gline(self._state))
        p.registerHandler("F", commands.info.info(self._state))
        p.registerHandler("I", commands.invite.invite(self._state))
        p.registerHandler("J", commands.join.join(self._state))
        p.registerHandler("JU", commands.jupe.jupe(self._state))
        p.registerHandler("K", commands.kick.kick(self._state))
        #p.registerHandler("D", commands.kill.kill(self._state))
        #p.registerHandler("LI", commands.links.links(self._state))
        #p.registerHandler("LU", commands.lusers.lusers(self._state))
        #p.registerHandler("M", commands.mode.mode(self._state))
        #p.registerHandler("MO", commands.motd.motd(self._state))
        #p.registerHandler("E", commands.names.names(self._state))
        p.registerHandler("N", commands.nick.nick(self._state))
        #p.registerHandler("O", commands.notice.notice(self._state))
        #p.registerHandler("OM", commands.opmode.opmode(self._state))
        #p.registerHandler("L", commands.part.part(self._state))
        #p.registerHandler("PASS", commands.password.password(self._state))
        #p.registerHandler("G", commands.ping.ping(self._state))
        #p.registerHandler("Z", commands.pong.pong(self._state))
        #p.registerHandler("P", commands.privmsg.privmsg(self._state))
        #p.registerHandler("Q", commands.quit.quit(self._state))
        #p.registerHandler("RI", commands.rping.rping(self._state))
        #p.registerHandler("RO", commands.rpong.rpong(self._state))
        #p.registerHandler("S", commands.server.server(self._state))
        #p.registerHandler("SE", commands.settime.settime(self._state))
        #p.registerHandler("U", commands.silence.silence(self._state))
        #p.registerHandler("SQ", commands.squit.squit(self._state))
        #p.registerHandler("R", commands.stats.stats(self._state))
        #p.registerHandler("SJ", commands.svsjoin.svsjoin(self._state))
        #p.registerHandler("SN", commands.svsnick.svsjoin(self._state))
        #p.registerHandler("TI", commands.time.time(self._state))
        #p.registerHandler("T", commands.topic.topic(self._state))
        #p.registerHandler("TR", commands.trace.trace(self._state))
        #p.registerHandler("UP", commands.uping.uping(self._state))
        #p.registerHandler("V", commands.version.version(self._state))
        #p.registerHandler("WC", commands.wallchops.wallchops(self._state))
        #p.registerHandler("WA", commands.wallops.wallops(self._state))
        #p.registerHandler("WU", commands.wallusers.wallusers(self._state))
        #p.registerHandler("WV", commands.wallvoices.wallvoices(self._state))
        #p.registerHandler("H", commands.who.who(self._state))
        #p.registerHandler("W", commands.whois.whois(self._state))
        #p.registerHandler("X", commands.whowas.whowas(self._state))
    
    def _sendLine(self, source_client, token, args):
        """ Send a line upsteam
        
            source_client: An integer, or None, representing which client is sending this message
            token: The token to be sent.
            args: An array of strings making up the message body """
        self._socket.sendall(self._parser.build(source_client, token, args))

class ConnectionError(Exception):
    """ When an error occurs in a connection """
    pass