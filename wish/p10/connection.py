"""
WISH - the WorldIRC Service Host

Handling connections to remote servers

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


# Things that aren't implemented:
# * RPING
# * RPONG
# * ASLL
# * UPING
# * WHOWAS

import asyncore
import fnmatch
import socket

from wish.p10.base64 import create_numeric, to_base64
from wish.p10.commands.account import AccountHandler
from wish.p10.commands.admin import AdminHandler
from wish.p10.commands.asll import AsllHandler
from wish.p10.commands.away import AwayHandler
from wish.p10.commands.burst import BurstHandler
from wish.p10.commands.clearmode import ClearModeHandler
from wish.p10.commands.connect import ConnectHandler
from wish.p10.commands.create import CreateHandler
from wish.p10.commands.destruct import DestructHandler
from wish.p10.commands.end_of_burst import EndOfBurstHandler
from wish.p10.commands.eob_ack import EobAckHandler
from wish.p10.commands.error import ErrorHandler
from wish.p10.commands.gline import GlineHandler
from wish.p10.commands.info import InfoHandler
from wish.p10.commands.invite import InviteHandler
from wish.p10.commands.join import JoinHandler
from wish.p10.commands.jupe import JupeHandler
from wish.p10.commands.kick import KickHandler
from wish.p10.commands.kill import KillHandler
from wish.p10.commands.links import LinksHandler
from wish.p10.commands.lusers import LusersHandler
from wish.p10.commands.mode import ModeHandler
from wish.p10.commands.motd import MotdHandler
from wish.p10.commands.names import NamesHandler
from wish.p10.commands.nick import NickHandler
from wish.p10.commands.notice import NoticeHandler
from wish.p10.commands.numberrelay import NumberRelayHandler
from wish.p10.commands.part import PartHandler
from wish.p10.commands.password import PasswordHandler
from wish.p10.commands.ping import PingHandler
from wish.p10.commands.pong import PongHandler
from wish.p10.commands.privmsg import PrivmsgHandler
from wish.p10.commands.quit import QuitHandler
#from wish.p10.commands.rping import RPingHandler
#from wish.p10.commands.rpong import RPongHandler
from wish.p10.commands.server import ServerHandler
from wish.p10.commands.settime import SetTimeHandler
from wish.p10.commands.silence import SilenceHandler
from wish.p10.commands.squit import SQuitHandler
from wish.p10.commands.stats import StatsHandler
from wish.p10.commands.svsjoin import SvsJoinHandler
from wish.p10.commands.svsnick import SvsNickHandler
from wish.p10.commands.time import TimeHandler
from wish.p10.commands.topic import TopicHandler
from wish.p10.commands.trace import TraceHandler
from wish.p10.commands.uping import UPingHandler
from wish.p10.commands.version import VersionHandler
from wish.p10.commands.wallchops import WallChOpsHandler
from wish.p10.commands.wallops import WallOpsHandler
from wish.p10.commands.wallusers import WallUsersHandler
from wish.p10.commands.wallvoices import WallVoicesHandler
from wish.p10.commands.whois import WhoIsHandler
from wish.p10.commands.whowas import WhoWasHandler
from wish.p10.errors import ConnectionError
from wish.p10.parser import Parser

class Connection(asyncore.dispatcher):
    """
    Represents a connection upstream
    """
    
    DISCONNECTED = 0
    CONNECTED = 1
    CHALLENGED = 2
    HANDSHAKE = 3
    AUTHENTICATED = 4
    COMPLETE = 5
    
    def __init__(self, state):
        """
        Sets up the state that this connection will alter
        """
        asyncore.dispatcher.__init__(self)
        self._state = state
        self.connstate = self.DISCONNECTED
        self.numeric = None
        self._upstream_password = None
        self._password = None
        self._endpoint = None
        self._parser =  Parser(state.max_client_numerics)
        self._buffer = ""
        self._data = ""
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self._last_ping = None
        self._last_pong = None
    
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
        self._buffer += "SERVER " \
                     + self._state.server_name \
                     + " 1 " + str(self._state.ts) \
                     + " " + str(self._state.ts) \
                     + " J10 " \
                     + create_numeric((self._state.server_id, 262143)) \
                     + " +s :" + self._state.server_description + "\r\n"
        self.connstate = self.CHALLENGED
        
        # Set up stuff for authentication
        self._parser.register_handler(
            "PASS", PasswordHandler(self._state, self))
        self._parser.register_handler("ERROR", ErrorHandler(self._state))
        self._last_pong = self._state.ts
        self._last_ping = self._state.ts
    
    def _setup_callbacks(self):
        self._state.register_callback(self._state.CALLBACK_NEWUSER,
                                      self.callback_new_user)
        self._state.register_callback(self._state.CALLBACK_CHANGENICK,
                                      self.callback_change_nick)
        self._state.register_callback(self._state.CALLBACK_NEWSERVER,
                                      self.callback_new_server)
        self._state.register_callback(self._state.CALLBACK_AUTHENTICATE,
                                      self.callback_authenticate)
        self._state.register_callback(self._state.CALLBACK_USERMODECHANGE,
                                      self.callback_change_user_mode)
        self._state.register_callback(self._state.CALLBACK_AWAY,
                                      self.callback_away)
        self._state.register_callback(self._state.CALLBACK_BACK,
                                      self.callback_back)
        self._state.register_callback(self._state.CALLBACK_CHANNELCREATE,
                                      self.callback_channel_create)
        self._state.register_callback(self._state.CALLBACK_CHANNELJOIN,
                                      self.callback_channel_join)
        self._state.register_callback(self._state.CALLBACK_CHANNELPART,
                                      self.callback_channel_part)
        self._state.register_callback(self._state.CALLBACK_CHANNELPARTALL,
                                      self.callback_part_all)
        self._state.register_callback(self._state.CALLBACK_CHANNELMODECHANGE,
                                      self.callback_channel_change_mode)
        self._state.register_callback(self._state.CALLBACK_CHANNELBANADD,
                                      self.callback_channel_add_ban)
        self._state.register_callback(self._state.CALLBACK_CHANNELBANREMOVE,
                                      self.callback_channel_remove_ban)
        self._state.register_callback(self._state.CALLBACK_CHANNELBANCLEAR,
                                      self.callback_channel_clear_bans)
        self._state.register_callback(self._state.CALLBACK_CHANNELOP,
                                      self.callback_channel_op)
        self._state.register_callback(self._state.CALLBACK_CHANNELDEOP,
                                      self.callback_channel_deop)
        self._state.register_callback(self._state.CALLBACK_CHANNELCLEAROPS,
                                      self.callback_channel_clear_ops)
        self._state.register_callback(self._state.CALLBACK_CHANNELVOICE,
                                      self.callback_channel_voice)
        self._state.register_callback(self._state.CALLBACK_CHANNELDEVOICE,
                                      self.callback_channel_devoice)
        self._state.register_callback(self._state.CALLBACK_CHANNELCLEARVOICES,
                                      self.callback_channel_clear_voices)
        self._state.register_callback(self._state.CALLBACK_GLINEADD,
                                      self.callback_gline_add)
        self._state.register_callback(self._state.CALLBACK_GLINEREMOVE,
                                      self.callback_gline_remove)
        self._state.register_callback(self._state.CALLBACK_INVITE,
                                      self.callback_invite)
        self._state.register_callback(self._state.CALLBACK_JUPEADD,
                                      self.callback_jupe_add)
        self._state.register_callback(self._state.CALLBACK_JUPEREMOVE,
                                      self.callback_jupe_remove)
        self._state.register_callback(self._state.CALLBACK_REQUESTADMIN,
                                      self.callback_admin_info)
        self._state.register_callback(self._state.CALLBACK_REQUESTINFO,
                                      self.callback_info_request)
        self._state.register_callback(self._state.CALLBACK_CHANNELKICK,
                                      self.callback_kick)
        self._state.register_callback(self._state.CALLBACK_CHANNELPARTZOMBIE,
                                      self.callback_zombie_part)
        self._state.register_callback(self._state.CALLBACK_CHANNELDESTROY,
                                      self.callback_channel_destroy)
        self._state.register_callback(self._state.CALLBACK_QUIT,
                                      self.callback_quit)
        self._state.register_callback(self._state.CALLBACK_KILL,
                                      self.callback_kill)
        self._state.register_callback(self._state.CALLBACK_REQUESTLUSERS,
                                      self.callback_lusers)
        self._state.register_callback(self._state.CALLBACK_REQUESTLINKS,
                                      self.callback_links)
        self._state.register_callback(self._state.CALLBACK_REQUESTMOTD,
                                      self.callback_motd)
        self._state.register_callback(self._state.CALLBACK_REQUESTNAMES,
                                      self.callback_names)
        self._state.register_callback(self._state.CALLBACK_CHANNELTOPIC,
                                      self.callback_topic)
        self._state.register_callback(self._state.CALLBACK_SILENCEADD,
                                      self.callback_silence_add)
        self._state.register_callback(self._state.CALLBACK_SILENCEREMOVE,
                                      self.callback_silence_remove)
        self._state.register_callback(self._state.CALLBACK_SERVERQUIT,
                                      self.callback_squit)
        self._state.register_callback(self._state.CALLBACK_REQUESTVERSION,
                                      self.callback_request_version)
        self._state.register_callback(self._state.CALLBACK_REQUESTSTATS,
                                      self.callback_request_stats)
        self._state.register_callback(self._state.CALLBACK_TRACE,
                                      self.callback_trace)
        self._state.register_callback(self._state.CALLBACK_PING,
                                      self.callback_ping)
        self._state.register_callback(self._state.CALLBACK_PONG,
                                      self.callback_pong)
        self._state.register_callback(self._state.CALLBACK_REQUESTWHOIS,
                                      self.callback_request_whois)
        self._state.register_callback(self._state.CALLBACK_PRIVMSG,
                                      self.callback_privmsg)
        self._state.register_callback(self._state.CALLBACK_OOBMSG,
                                      self.callback_oobmsg)
        self._state.register_callback(self._state.CALLBACK_NOTICE,
                                      self.callback_notice)
        self._state.register_callback(self._state.CALLBACK_WALLOPS,
                                      self.callback_wallops)
        self._state.register_callback(self._state.CALLBACK_WALLUSERS,
                                      self.callback_wallusers)
        self._state.register_callback(self._state.CALLBACK_WALLVOICES,
                                      self.callback_wallvoices)
        self._state.register_callback(self._state.CALLBACK_WALLCHOPS,
                                      self.callback_wallchops)
    
    def _teardown_callbacks(self):
        self._state.deregister_callback(self._state.CALLBACK_NEWUSER,
                                        self.callback_new_user)
        self._state.deregister_callback(self._state.CALLBACK_CHANGENICK,
                                        self.callback_change_nick)
        self._state.deregister_callback(self._state.CALLBACK_NEWSERVER,
                                        self.callback_new_server)
        self._state.deregister_callback(self._state.CALLBACK_AUTHENTICATE,
                                        self.callback_authenticate)
        self._state.deregister_callback(self._state.CALLBACK_USERMODECHANGE,
                                        self.callback_change_user_mode)
        self._state.deregister_callback(self._state.CALLBACK_AWAY,
                                        self.callback_away)
        self._state.deregister_callback(self._state.CALLBACK_BACK,
                                        self.callback_back)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELCREATE,
                                        self.callback_channel_create)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELJOIN,
                                        self.callback_channel_join)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELPART,
                                        self.callback_channel_part)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELPARTALL,
                                        self.callback_part_all)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELMODECHANGE,
                                        self.callback_channel_change_mode)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELBANADD,
                                        self.callback_channel_add_ban)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELBANREMOVE,
                                        self.callback_channel_remove_ban)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELBANCLEAR,
                                        self.callback_channel_clear_bans)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELOP,
                                        self.callback_channel_op)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELDEOP,
                                        self.callback_channel_deop)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELCLEAROPS,
                                        self.callback_channel_clear_ops)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELVOICE,
                                        self.callback_channel_voice)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELDEVOICE,
                                        self.callback_channel_devoice)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELCLEARVOICES,
                                        self.callback_channel_clear_voices)
        self._state.deregister_callback(self._state.CALLBACK_GLINEADD,
                                        self.callback_gline_add)
        self._state.deregister_callback(self._state.CALLBACK_GLINEREMOVE,
                                        self.callback_gline_remove)
        self._state.deregister_callback(self._state.CALLBACK_INVITE,
                                        self.callback_invite)
        self._state.deregister_callback(self._state.CALLBACK_JUPEADD,
                                        self.callback_jupe_add)
        self._state.deregister_callback(self._state.CALLBACK_JUPEREMOVE,
                                        self.callback_jupe_remove)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTADMIN,
                                        self.callback_admin_info)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTINFO,
                                        self.callback_info_request)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELKICK,
                                        self.callback_kick)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELPARTZOMBIE,
                                        self.callback_zombie_part)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELDESTROY,
                                        self.callback_channel_destroy)
        self._state.deregister_callback(self._state.CALLBACK_QUIT,
                                        self.callback_quit)
        self._state.deregister_callback(self._state.CALLBACK_KILL,
                                        self.callback_kill)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTLUSERS,
                                        self.callback_lusers)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTLINKS,
                                        self.callback_links)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTMOTD,
                                        self.callback_motd)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTNAMES,
                                        self.callback_names)
        self._state.deregister_callback(self._state.CALLBACK_CHANNELTOPIC,
                                        self.callback_topic)
        self._state.deregister_callback(self._state.CALLBACK_SILENCEADD,
                                        self.callback_silence_add)
        self._state.deregister_callback(self._state.CALLBACK_SILENCEREMOVE,
                                        self.callback_silence_remove)
        self._state.deregister_callback(self._state.CALLBACK_SERVERQUIT,
                                        self.callback_squit)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTVERSION,
                                        self.callback_request_version)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTSTATS,
                                        self.callback_request_stats)
        self._state.deregister_callback(self._state.CALLBACK_TRACE,
                                        self.callback_trace)
        self._state.deregister_callback(self._state.CALLBACK_PING,
                                        self.callback_ping)
        self._state.deregister_callback(self._state.CALLBACK_PONG,
                                        self.callback_pong)
        self._state.deregister_callback(self._state.CALLBACK_REQUESTWHOIS,
                                        self.callback_request_whois)
        self._state.deregister_callback(self._state.CALLBACK_PRIVMSG,
                                        self.callback_privmsg)
        self._state.deregister_callback(self._state.CALLBACK_OOBMSG,
                                        self.callback_oobmsg)
        self._state.deregister_callback(self._state.CALLBACK_NOTICE,
                                        self.callback_notice)
        self._state.deregister_callback(self._state.CALLBACK_WALLOPS,
                                        self.callback_wallops)
        self._state.deregister_callback(self._state.CALLBACK_WALLUSERS,
                                        self.callback_wallusers)
        self._state.deregister_callback(self._state.CALLBACK_WALLVOICES,
                                        self.callback_wallvoices)
        self._state.deregister_callback(self._state.CALLBACK_WALLCHOPS,
                                        self.callback_wallchops)
    
    def _setup_parser(self):
        p = self._parser
        p.register_handler("AC", AccountHandler(self._state))
        p.register_handler("AD", AdminHandler(self._state))
        p.register_handler("LL", AsllHandler(self._state))
        p.register_handler("A", AwayHandler(self._state))
        p.register_handler("B", BurstHandler(self._state))
        p.register_handler("CM", ClearModeHandler(self._state))
        p.register_handler("CO", ConnectHandler(self._state))
        p.register_handler("C", CreateHandler(self._state))
        p.register_handler("DE", DestructHandler(self._state))
        p.register_handler("DS", WallOpsHandler(self._state))
        p.register_handler("EB", EndOfBurstHandler(self._state, self))
        p.register_handler("EA", EobAckHandler(self._state))
        p.register_handler("Y", ErrorHandler(self._state))
        p.register_handler("GL", GlineHandler(self._state))
        p.register_handler("F", InfoHandler(self._state))
        p.register_handler("I", InviteHandler(self._state))
        p.register_handler("J", JoinHandler(self._state))
        p.register_handler("JU", JupeHandler(self._state))
        p.register_handler("K", KickHandler(self._state))
        p.register_handler("D", KillHandler(self._state))
        p.register_handler("LI", LinksHandler(self._state))
        p.register_handler("LU", LusersHandler(self._state))
        p.register_handler("M", ModeHandler(self._state))
        p.register_handler("MO", MotdHandler(self._state))
        p.register_handler("E", NamesHandler(self._state))
        p.register_handler("N", NickHandler(self._state))
        p.register_handler("O", NoticeHandler(self._state))
        # opmodes get handled exactly the same as normal modes
        p.register_handler("OM", ModeHandler(self._state)) 
        p.register_handler("L", PartHandler(self._state))
        p.register_handler("G", PingHandler(self._state, self))
        p.register_handler("Z", PongHandler(self._state, self))
        p.register_handler("P", PrivmsgHandler(self._state))
        p.register_handler("Q", QuitHandler(self._state))
        #p.register_handler("RI", RPingHandler(self._state))
        #p.register_handler("RO", RPong(self._state))
        p.register_handler("S", ServerHandler(self._state, None))
        p.register_handler("SE", SetTimeHandler(self._state))
        p.register_handler("U", SilenceHandler(self._state))
        p.register_handler("SQ", SQuitHandler(self._state))
        p.register_handler("R", StatsHandler(self._state))
        p.register_handler("SJ", SvsJoinHandler(self._state))
        p.register_handler("SN", SvsNickHandler(self._state))
        p.register_handler("TI", TimeHandler(self._state))
        p.register_handler("T", TopicHandler(self._state))
        p.register_handler("TR", TraceHandler(self._state))
        p.register_handler("UP", UPingHandler(self._state))
        p.register_handler("V", VersionHandler(self._state))
        p.register_handler("WC", WallChOpsHandler(self._state))
        p.register_handler("WA", WallOpsHandler(self._state))
        p.register_handler("WU", WallUsersHandler(self._state))
        p.register_handler("WV", WallVoicesHandler(self._state))
        p.register_handler("W", WhoIsHandler(self._state))
        p.register_handler("X", WhoWasHandler(self._state))
        p.register_handler("252", NumberRelayHandler(self._state, "252"))
        p.register_handler("254", NumberRelayHandler(self._state, "254"))
        p.register_handler("255", NumberRelayHandler(self._state, "255"))
        p.register_handler("256", NumberRelayHandler(self._state, "256"))
        p.register_handler("257", NumberRelayHandler(self._state, "257"))
        p.register_handler("258", NumberRelayHandler(self._state, "258"))
        p.register_handler("259", NumberRelayHandler(self._state, "259"))
        p.register_handler("351", NumberRelayHandler(self._state, "351"))
        p.register_handler("353", NumberRelayHandler(self._state, "353"))
        p.register_handler("364", NumberRelayHandler(self._state, "364"))
        p.register_handler("365", NumberRelayHandler(self._state, "365"))
        p.register_handler("366", NumberRelayHandler(self._state, "366"))
        p.register_handler("371", NumberRelayHandler(self._state, "371"))
        p.register_handler("374", NumberRelayHandler(self._state, "374"))
        p.register_handler("375", NumberRelayHandler(self._state, "375"))
        p.register_handler("376", NumberRelayHandler(self._state, "376"))
    
    def _send_line(self, source_client, token, args):
        """
        Send a line upsteam
        
        source_client: An integer, or None, representing which client is sending this message
        token: The token to be sent.
        args: An array of strings making up the message body
        """
        self._buffer += self._parser.build(source_client, token, args)
    
    def register_numeric(self, numeric):
        self.numeric = numeric
    
    def register_upstream_password(self, password):
        self._upstream_password = password
    
    def register_eob(self):
        self._send_line((self._state.server_id, None), "EA", [])
    
    def register_ping(self, arg):
        self._send_line(
            (self._state.server_id, None),
            "Z",
            [create_numeric((self._state.server_id, None)), arg]
        )
    
    def register_pong(self):
        self._last_pong = self._state.ts
    
    def close_connection(self):
        self.close()
        self.connstate = self.COMPLETE
    
    def do_ping(self):
        # Give a 60 second grace between ping being sent and timing out
        if (self._state.ts - 60) > self._last_ping \
        and self._last_ping > self._last_pong:
            self.error("Ping Timeout")
        elif self._last_ping < (self._state.ts - 180):
            self._send_line(
                (self._state.server_id, None),
                "G",
                [create_numeric((self._state.server_id, None))]
            )
            self._last_ping = self._state.ts
    
    def error(self, reason):
        """ TODO: Handles errors on the connection """
        print "ERROR: " + reason
        self._send_line(
            (self._state.server_id, None),
            "Y",
            [reason]
        )
    
    def _recursive_burst_server(self, server):
        # We don't burst ourselves
        if self._state.servers[server].numeric != self._state.server_id:
            self.callback_new_server(
                (self._state.servers[server].origin, None),
                self._state.servers[server].numeric,
                self._state.servers[server].name,
                self._state.servers[server].maxclient,
                self._state.servers[server].boot_ts,
                self._state.servers[server].link_ts,
                self._state.servers[server].protocol,
                self._state.servers[server].hops,
                self._state.servers[server].flags,
                self._state.servers[server].description
            )
        for child in self._state.servers[server].children:
            # Don't burst the server back to us
            if child != self.numeric:
                self._recursive_burst_server(child)
    
    def _send_burst(self):
        # Now we start listening
        self._setup_callbacks()
        
        # Send servers
        self._recursive_burst_server(self._state.server_id)
        
        # Send g-lines
        for (mask, desc, expires, active, mod_time) in self._state.glines:
            if active:
                self.callback_gline_add(
                    (self._state.server_id, None),
                    mask,
                    None,
                    expires,
                    desc
                )
            else:
                self.callback_gline_remove(
                    (self._state.server_id, None),
                    mask,
                    None
                )
        
        # Send jupes
        for (mask, description, expires, active, mod_time) in self._state.jupes:
            if active:
                self.callback_jupe_add(
                    (self._state.server_id, None),
                    mask,
                    None,
                    expires,
                    description
                )
            else:
                self.callback_jupe_remove(
                    (self._state.server_id, None),
                    mask,
                    None
                )
        
        # Send users
        for user in self._state.users:
            self.callback_new_user(
                (self._state.users[user].numeric[0], None),
                self._state.users[user].numeric,
                self._state.users[user].nickname,
                self._state.users[user].username,
                self._state.users[user].hostname,
                self._state.users[user].modes,
                self._state.users[user].ip,
                self._state.users[user].hops,
                self._state.users[user].ts,
                self._state.users[user].fullname
            )
        
        # Send channels
        for channel in self._state.channels:
            
            # First part of burst
            burst = [channel, str(self._state.channels[channel].ts)]
            
            # Channel modes
            (modestr, modeargs) = self._build_mode_string(
                self._state.channels[channel].modes)
            
            if modestr != "":
                burst.append(modestr)
            burst += modeargs
            
            # Get users on channel
            users = self._state.channels[channel].users
            ovs = []
            os = []
            vs = []
            plains = []
            for user in users:
                numeric = create_numeric(user)
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
                
                self._send_line((self._state.server_id, None), "B", burst)
                burst = [channel, str(self._state.channels[channel].ts)]
                
                # Check we're done
                if len(plains) == 0 and len(vs) == 0 and len(os) == 0 \
                and len(ovs) == 0 and len(bans) == 0:
                    done = True
        
        self._send_line((self._state.server_id, None), "EB", [])
    
    def writable(self):
        return (len(self._buffer) > 0)
    
    def handle_write(self):
        sent = self.send(self._buffer)
        print "SENT: " + self._buffer[:sent]
        self._buffer = self._buffer[sent:]
    
    def handle_close(self):
        if self.connstate != self.COMPLETE:
            self._state.quit_server(
                (self._state.server_id, None),
                (self.numeric, None),
                "Connection closed unexpectedly",
                self._state.ts
            )
            self.connstate = self.COMPLETE
        self._teardown_callbacks()
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
            if self.connstate == self.CHALLENGED \
            and self._upstream_password != None:
                # Check password
                if self._password == self._upstream_password:
                    self.connstate = self.HANDSHAKE
                    self._parser.register_handler(
                        "SERVER", ServerHandler(self._state, self))
                else:
                    self.error("Password not as expected")
            if self.connstate == self.HANDSHAKE and self.numeric != None:
                self.connstate = self.AUTHENTICATED
                self._setup_parser()
                # We're all good, send netburst
                self._send_burst()
            if self.connstate < self.AUTHENTICATED:
                try:
                    self._parser.parse_pre_auth(
                        line, (self._state.server_id, None))
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
    
    def _build_mode_string(self, modes):
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
    
    def callback_new_user(self, origin, numeric, nickname, username, hostname,
                          modes, ip, hops, ts, fullname):
        # Broadcast to all away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            line = [nickname, str(hops + 1), str(ts), username, hostname]
            (modestr, modeargs) = self._build_mode_string(modes)
            if modestr != "":
                line.append(modestr)
            line += modeargs
            line.append(to_base64(ip, 6))
            line.append(create_numeric(numeric))
            line.append(fullname)
            self._send_line(origin, "N", line)
    
    def callback_change_nick(self, origin, numeric, newnick, newts):
        # Broadcast to all away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            if origin != numeric:
                self._send_line(
                    origin, "SN", [create_numeric(numeric), newnick])
            else:
                self._send_line(numeric, "N", [newnick, str(newts)])
    
    def callback_new_server(self, origin, numeric, name, maxclient, boot_ts,
                            link_ts, protocol, hops, flags, description):
        # Broadcast to all away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            (modestr, modeargs) = self._build_mode_string(flags)
            if modestr == '':
                modestr = '+'
            self._send_line(
                origin, "S", [
                    name,
                    str(hops + 1),
                    str(boot_ts),
                    str(link_ts),
                    protocol,
                    create_numeric((numeric, maxclient)),
                    modestr,
                    description
                ]
            )
    
    def callback_squit(self, origin, numeric, reason, ts):
        # If this uplink is the one being disconnected
        if numeric[0] == self.numeric:
            self.close_connection()
            self._send_line(origin, "SQ",
                            [self._state.server_name, "0", reason])
        # Otherwise, broadcast away from origin
        elif self._state.get_next_hop(origin) != self.numeric:
            self._send_line(
                origin, "SQ",
                [
                    self._state.numeric2nick(numeric),
                    str(ts),
                    reason
                ]
            )
    
    def callback_authenticate(self, origin, numeric, acname):
        # Broadcast to all away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "AC", [create_numeric(numeric), acname])
    
    def callback_away(self, numeric, reason):
        # Broadcast to all away from origin
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "A", [reason])
    
    def callback_back(self, numeric):
        # Broadcast to all away from origin
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "A", [])
    
    def callback_channel_create(self, origin, name, ts):
        # Broadcast to all servers away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "C", [name, str(ts)])
    
    def callback_channel_join(self, origin, numeric, name, modes, ts):
        # Broadcast to all servers away from origin
        if self._state.get_next_hop(origin) != self.numeric:
            # If it's a forced join, must be a SJ
            if origin != numeric:
                self._send_line(origin, "SJ", [create_numeric(numeric), name])
            else:
                self._send_line(origin, "J", [name, str(ts)])
            # In theory, joins should never be called if the channel already
            # exists so we must force any modes on
            if "o" in modes:
                self.callback_channel_op(origin, name, numeric)
            if "v" in modes:
                self.callback_channel_voice(origin, name, numeric)
    
    def callback_channel_part(self, numeric, name, reason):
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "P", [name, reason])
    
    def callback_part_all(self, numeric):
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "J", ["0"])
    
    def callback_channel_change_mode(self, origin, name, modes):
        if self._state.get_next_hop(origin) != self.numeric:
            line = [name]
            (modestr, modeargs) = self._build_mode_string(modes)
            line.append(modestr)
            line += modeargs
            line.append(str(self._state.channels[name].ts))
            self._send_line(origin, "M", line)
    
    def callback_channel_add_ban(self, origin, name, mask):
        self.callback_channel_change_mode(origin, name, [("+b", mask)])
    
    def callback_channel_remove_ban(self, origin, name, ban):
        self.callback_channel_change_mode(origin, name, [("-b", ban)])
    
    def callback_channel_clear_bans(self, origin, name):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "CM", [name, "b"])
    
    def callback_channel_op(self, origin, channel, user):
        self.callback_channel_change_mode(
            origin, channel, [("+o", create_numeric(user))])
    
    def callback_channel_deop(self, origin, channel, user):
        self.callback_channel_change_mode(
            origin, channel, [("-o", create_numeric(user))])
    
    def callback_channel_clear_ops(self, origin, name):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "CM", [name, "o"])
    
    def callback_channel_voice(self, origin, channel, user):
        self.callback_channel_change_mode(
            origin, channel, [("+v", create_numeric(user))])
    
    def callback_channel_devoice(self, origin, channel, user):
        self.callback_channel_change_mode(
            origin, channel, [("-v", create_numeric(user))])
    
    def callback_channel_clear_voices(self, origin, name):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "CM", [name, "v"])
    
    def _get_gline(self, mask):
        for gline in self._state.glines:
            if mask == gline[0]:
                return gline
    
    def callback_gline_add(self, origin, mask, target, expires, description):
        gline = self._get_gline(mask)
        if self._state.get_next_hop(origin) != self.numeric and target == None:
            self._send_line(
                origin, "GL",
                [
                    "*",
                    "+" + mask,
                    str(expires - gline[4]),
                    str(gline[4]),
                    description
                ]
            )
        elif self._state.get_next_hop((target, None)) == self.numeric:
            self._send_line(
                origin, "GL",
                [
                    create_numeric((target, None)),
                    "+" + mask,
                    str(expires - gline[4]),
                    str(gline[4]),
                    description
                ]
            )
    
    def callback_gline_remove(self, origin, mask, target):
        gline = self._get_gline(mask)
        if self._state.get_next_hop(origin) != self.numeric and target == None:
            self._send_line(
                origin, "GL",
                [
                    "*",
                    "-" + mask,
                    str(gline[2] - gline[4]),
                    str(gline[4]),
                    gline[1]
                ]
            )
        elif self._state.get_next_hop((target, None)) == self.numeric:
            self._send_line(
                origin, "GL",
                [
                    create_numeric((target, None)),
                    "-" + mask,
                    str(gline[2] - gline[4]),
                    str(gline[4]),
                    gline[1]
                ]
            )
    
    def callback_invite(self, origin, target, channel):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(
                origin, "I", [self._state.numeric2nick(target), channel])
    
    def _get_jupe(self, server):
        for jupe in self._state.jupes:
            if server == jupe[0]:
                return jupe
    
    def callback_jupe_add(self, origin, server, target, expire, reason):
        jupe = self._get_jupe(server)
        if self._state.get_next_hop(origin) != self.numeric and target == None:
            self._send_line(
                origin, "JU",
                [
                    "*",
                    "+" + server,
                    str(expire - jupe[4]),
                    str(jupe[4]),
                    reason
                ]
            )
        elif self._state.get_next_hop((target, None)) == self.numeric:
            self._send_line(
                origin, "JU",
                [
                    create_numeric((target, None)),
                    "+" + server,
                    str(expire - jupe[4]),
                    str(jupe[4]),
                    reason
                ]
            )
    
    def callback_jupe_remove(self, origin, server, target):
        jupe = self._get_jupe(server)
        if self._state.get_next_hop(origin) != self.numeric and target == None:
            self._send_line(
                origin, "JU",
                [
                    "*",
                    "-" + server,
                    str(jupe[2] - jupe[4]),
                    str(jupe[4]),
                    jupe[1]
                ]
            )
        elif self._state.get_next_hop((target, None)) == self.numeric:
            self._send_line(
                origin, "JU",
                [
                    create_numeric((target, None)),
                    "-" + server,
                    str(jupe[2] - jupe[4]),
                    str(jupe[4]),
                    jupe[1]
                ]
            )
    
    def callback_admin_info(self, origin, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "AD", [create_numeric(target)])
    
    def callback_info_request(self, origin, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "F", [create_numeric(target)])
    
    def callback_kick(self, origin, channel, target, reason):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "K",
                            [channel, create_numeric(target), reason])
    
    def callback_zombie_part(self, origin, channel):
        self.callback_channel_part(origin, channel, "Zombie parting channel")
    
    def callback_channel_destroy(self, origin, channel, ts):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "DE", [channel, str(ts)])
    
    def callback_quit(self, numeric, reason, causedbysquit):
        if not causedbysquit and \
          self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "Q", [reason])
    
    def callback_kill(self, origin, target, path, reason):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(
                origin, "D",
                [create_numeric(target), "!".join(path) + " (" + reason + ")"]
            )
    
    def callback_lusers(self, origin, target, dummy):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "LU", [dummy, create_numeric(target)])
    
    def callback_links(self, origin, target, mask):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "LI", [create_numeric(target), mask])
    
    def callback_change_user_mode(self, numeric, modes):
        if self._state.get_next_hop(numeric) != self.numeric:
            line = [self._state.numeric2nick(numeric)]
            (modestr, modeargs) = self._build_mode_string(modes)
            line.append(modestr)
            line += modeargs
            self._send_line(numeric, "M", line)
    
    def callback_motd(self, numeric, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(numeric, "MO", [create_numeric(target)])
    
    def callback_names(self, origin, target, channels):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "E",
                            [",".join(channels), create_numeric(target)])
    
    def callback_topic(self, origin, channel, topic, topic_ts, channel_ts):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "T",
                            [channel, str(channel_ts), str(topic_ts), topic])
    
    def callback_silence_add(self, numeric, mask):
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "U", ["*", mask])
    
    def callback_silence_remove(self, numeric, mask):
        if self._state.get_next_hop(numeric) != self.numeric:
            self._send_line(numeric, "U", ["*", "-" + mask])
    
    def callback_request_version(self, origin, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "V", [create_numeric(target)])
    
    def callback_request_stats(self, origin, target, stat, arg):
        if self._state.get_next_hop(target) == self.numeric:
            if arg != None:
                self._send_line(origin, "R",
                                [stat, create_numeric(target), arg])
            else:
                self._send_line(origin, "R", [stat, create_numeric(target)])
    
    def callback_trace(self, origin, search, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "TR", [search, create_numeric(target)])
    
    def callback_ping(self, origin, source, target):
        if target[0] == self._state.server_id \
        and self._state.get_next_hop(origin) == self.numeric:
            self._send_line(
                (self._state.server_id, None), "Z",
                [create_numeric((self._state.server_id, None)), source]
            )
        elif self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "G", [source, create_numeric(target)])
    
    def callback_pong(self, origin, source, target):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "Z",
                            [create_numeric(source), create_numeric(target)])
    
    def callback_request_whois(self, origin, target, search):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, "W", [create_numeric(target), search])
    
    def _multi_target_message(self, origin, target, message_type, message):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, message_type, [create_numeric(target), message])
        elif target[0] == "#":
            if self._state.get_next_hop(origin) != self.numeric:
                for user in self._state.channels[target].users:
                    if self._state.get_next_hop(user) == self.numeric:
                        self._send_line(origin, message_type, [target, message])
                        return
        elif "@" in target:
            target_parts = target.split("@")
            target_numeric = self._state.nick2numeric(target_parts[1])
            if self._state.get_next_hop(target_numeric) == self.numeric:
                self._send_line(origin, message_type, [target, message])
        elif "$" in target:
            mask = target[1:]
            for server in self._state.servers:
                if self._state.get_next_hop((server, None)) == self.numeric \
                and fnmatch.fnmatch(self._state.servers[server].name, mask):
                    self._send_line(origin, message_type, [target, message])
                    return
    
    def callback_privmsg(self, origin, target, message):
        self._multi_target_message(origin, target, "P", message)
    
    def callback_notice(self, origin, target, message):
        self._multi_target_message(origin, target, "O", message)
    
    def callback_oobmsg(self, origin, target, type, args):
        if self._state.get_next_hop(target) == self.numeric:
            self._send_line(origin, type, [create_numeric(target)] + args)
    
    def callback_wallops(self, origin, message):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "WA", [message])
    
    def callback_wallusers(self, origin, message):
        if self._state.get_next_hop(origin) != self.numeric:
            self._send_line(origin, "WU", [message])
    
    def callback_wallvoices(self, origin, channel, message):
        if self._state.get_next_hop(origin) != self.numeric:
            for user in self._state.channels[channel].users:
                if self._state.get_next_hop(user) == self.numeric and \
                (self._state.channels[channel].isvoice(user) \
                 or self._state.channels[channel].isop(user)):
                    self._send_line(origin, "WV", [channel, message])
                    return
        
    def callback_wallchops(self, origin, channel, message):
        if self._state.get_next_hop(origin) != self.numeric:
            for user in self._state.channels[channel].users:
                if self._state.get_next_hop(user) == self.numeric \
                and self._state.channels[channel].isop(user):
                    self._send_line(origin, "WC", [channel, message])
                    return
