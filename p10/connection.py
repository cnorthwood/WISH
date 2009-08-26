#!/usr/bin/env python

import threading
import asyncore
import socket

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
    _connstate = None
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
    
    def __init__(self, state):
        """ Sets up the state that this connection will alter """
        asyncore.dispatcher.__init__(self)
        self._state = state
        self._connstate = self.DISCONNECTED
        self.numeric = None
        self._upstream_password = None
        self._password = None
        self._endpoint = None
        self._parser =  parser.parser(state.maxClientNumerics)
        self._buffer = ""
        self._data = ""
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _connect(self):
        self.connect(self._endpoint)
        self._connstate = self.CONNECTED
        print "Connecting to endpoint"

        # Send pass and server - don't use the parser at this point
        self._buffer += "PASS :" + self._password + "\r\n"
        self._buffer += "SERVER " + self._state.getServerName() + " 1 " + str(self._state.ts()) + " " + str(self._state.ts()) + " J10 " + base64.createNumeric((self._state.getServerID(), 262143)) + " +s :" + self._state.getServerName() + "\r\n"
        self._connstate = self.CHALLENGED
        
        # Set up stuff for authentication
        self._parser.registerHandler("PASS", commands.password.password(self._state, self))
        self._parser.registerHandler("ERROR", commands.error.error(self._state))
        self._last_pong = self._state.ts()
        self._last_ping = self._state.ts()
    
    def start(self, endpoint, password):
        # Create our socket
        self._endpoint = endpoint
        self._password = password
        self._connect()
        return self
    
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
        #p.registerHandler("SE", commands.settime.settime(self._state))
        p.registerHandler("U", commands.silence.silence(self._state))
        p.registerHandler("SQ", commands.squit.squit(self._state))
        #p.registerHandler("R", commands.stats.stats(self._state))
        p.registerHandler("SJ", commands.svsjoin.svsjoin(self._state))
        p.registerHandler("SN", commands.svsnick.svsnick(self._state))
        #p.registerHandler("TI", commands.time.time(self._state))
        p.registerHandler("T", commands.topic.topic(self._state))
        #p.registerHandler("TR", commands.trace.trace(self._state))
        #p.registerHandler("UP", commands.uping.uping(self._state))
        #p.registerHandler("V", commands.version.version(self._state))
        p.registerHandler("WC", commands.wallchops.wallchops(self._state))
        p.registerHandler("WA", commands.wallops.wallops(self._state))
        p.registerHandler("WU", commands.wallusers.wallusers(self._state))
        p.registerHandler("WV", commands.wallvoices.wallvoices(self._state))
        p.registerHandler("W", commands.whois.whois(self._state))
        p.registerHandler("X", commands.whowas.whowas(self._state))
    
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
        self._sendLine((self._state.getServerID(), None), "Z", [str(self._state.getServerID()), arg])
        print "PING? PONG!"
    
    def registerPong(self):
        self._last_pong = self._state.ts()
        print "PONG!"
    
    def do_ping(self):
        # Give a 60 second grace between ping being sent and timing out
        if (self._state.ts() - 60) > self._last_ping and self._last_ping > self._last_pong:
            print "Last ping received: " + str(self._last_ping)
            print "Last pong received: " + str(self._last_pong)
            print "Time now: " + str(self._state.ts())
            self.error("Ping Timeout")
        elif self._last_ping < (self._state.ts() - 180):
            print "PING!"
            self._sendLine((self._state.getServerID(), None), "G", [base64.createNumeric((self._state.getServerID(), None))])
            self._last_ping = self._state.ts()
    
    def error(self, reason):
        """ TODO: Handles errors on the connection """
        print "ERROR: " + reason
        self._sendLine((self._state.getServerID(), None), "Y", [reason])
        
    def _sendBurst(self):
        self._sendLine((self._state.getServerID(), None), "EB", [])
    
    def writable(self):
        return (len(self._buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self._buffer)
        print "SENT: " + self._buffer[:sent]
        self._buffer = self._buffer[sent:]
        
    def handle_close(self):
        self.close()
        # Now reconnect!
        self._reconnect()

    def handle_read(self):
        # Get this chunk
        self._data += self.recv(512)

        # Get an entire line
        nlb = self._data.find("\n")
        while nlb > -1:
            line = self._data[:nlb+1]
            print "HANDLING: " + line
            # Update state
            if self._connstate == self.CHALLENGED and self._upstream_password != None:
                # Check password
                if self._password == self._upstream_password:
                    self._connstate = self.HANDSHAKE
                    self._parser.registerHandler("SERVER", commands.server.server(self._state, self))
                else:
                    self.error("Password not as expected")
            if self._connstate == self.HANDSHAKE and self.numeric != None:
                self._connstate = self.AUTHENTICATED
                self._setupParser()
                # We're all good, send netburst
                self._sendBurst()
            if self._connstate < self.AUTHENTICATED:
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



class ConnectionError(Exception):
    """ When an error occurs in a connection """
    pass
