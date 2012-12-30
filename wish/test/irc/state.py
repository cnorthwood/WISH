#!/usr/bin/env python
"""
WISH - the WorldIRC Service Host

Unit tests for server state

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


import unittest

from wish.irc.state import State, StateError
from wish.p10.parser import Parser, ProtocolError

class ConfigDouble():
    """
    Mock config
    """
    
    numeric_id = 1
    server_name = "example.com"
    admin_nick = "test"
    contact_email = "test@example.com"
    called = False
    hidden_user_mask = ".users.example.com"
    server_description = "Example test"

class ConnectionDouble():
    """
    Mock connection - can interrogate the callbacks attribute to determine
    what callbacks have been called
    """
    
    def __init__(self):
        self.callbacks = []
        
    def callback_new_user(self, *args):
        self.callbacks.append("new_user")
        
    def callback_change_nick(self, *args):
        self.callbacks.append("ChangeNick")
    
    def callback_new_server(self, *args):
        self.callbacks.append("NewServer")
    
    def callback_squit(self, *args):
        self.callbacks.append("Squit")
    
    def callback_authenticate(self, origin, numeric, acname):
        self.callbacks.append("Authenticate")
    
    def callback_away(self, numeric, reason):
        self.callbacks.append("Away")
    
    def callback_back(self, numeric):
        self.callbacks.append("Back")
    
    def callback_channel_create(self, origin, name, ts):
        self.callbacks.append("ChannelCreate")
    
    def callback_channel_join(self, origin, numeric, name, modes, ts):
        self.callbacks.append("ChannelJoin")
    
    def callback_channel_part(self, numeric, name, reason):
        self.callbacks.append("ChannelPart")
    
    def callback_part_all(self, numeric):
        self.callbacks.append("PartAll")
    
    def callback_channel_change_mode(self, origin, name, mode):
        self.callbacks.append("ChannelChangeMode")
    
    def callback_channel_add_ban(self, origin, name, mask):
        self.callbacks.append("BanAdd")
    
    def callback_channel_remove_ban(self, origin, name, ban):
        self.callbacks.append("BanRemove")
    
    def callback_channel_clear_bans(self, origin, name):
        self.callbacks.append("ClearBans")
    
    def callback_channel_op(self, origin, channel, user):
        self.callbacks.append("Op")
    
    def callback_channel_deop(self, origin, channel, user):
        self.callbacks.append("Deop")
    
    def callback_channel_clear_ops(self, origin, name):
        self.callbacks.append("ClearOps")
    
    def callback_channel_voice(self, origin, channel, user):
        self.callbacks.append("Voice")
    
    def callback_channel_devoice(self, origin, channel, user):
        self.callbacks.append("Devoice")
    
    def callback_channel_clear_voices(self, origin, name):
        self.callbacks.append("ClearVoices")
    
    def callback_gline_add(self, origin, mask, target, expires, description):
        self.callbacks.append("GlineAdd")
    
    def callback_gline_remove(self, origin, mask, target):
        self.callbacks.append("GlineRemove")
    
    def callback_invite(self, origin, target, channel):
        self.callbacks.append("Invite")
    
    def callback_jupe_add(self, origin, server, target, expire, reason):
        self.callbacks.append("JupeAdd")
    
    def callback_jupe_remove(self, origin, server, target):
        self.callbacks.append("JupeRemove")
    
    def callback_admin_info(self, origin, target):
        self.callbacks.append("RequestAdmin")
    
    def callback_info_request(self, origin, target):
        self.callbacks.append("RequestInfo")
    
    def callback_kick(self, origin, channel, target, reason):
        self.callbacks.append("ChannelKick")
    
    def callback_zombie_part(self, origin, target):
        self.callbacks.append("ChannelPartZombie")
    
    def callback_channel_destroy(self, origin, channel, ts):
        self.callbacks.append("DestroyChannel")
    
    def callback_quit(self, numeric, reason, causedbysquit):
        if not causedbysquit:
            self.callbacks.append(("Quit", reason))
    
    def callback_kill(self, origin, target, path, reason):
        self.callbacks.append(("Kill", path, reason))
    
    def callback_lusers(self, origin, target, dummy):
        self.callbacks.append("Lusers")
    
    def callback_links(self, origin, target, mask):
        self.callbacks.append("Links")
    
    def callback_change_user_mode(self, numeric, modes):
        self.callbacks.append("ChangeUserMode")
    
    def callback_motd(self, numeric, target):
        self.callbacks.append("MOTD")
    
    def callback_names(self, origin, target, channel):
        self.callbacks.append("Names")
    
    def callback_topic(self, origin, channel, topic, topic_ts, channel_ts):
        self.callbacks.append("Topic")
    
    def callback_silence_add(self, numeric, mask):
        self.callbacks.append("SilenceAdd")
    
    def callback_silence_remove(self, numeric, mask):
        self.callbacks.append("SilenceRemove")
    
    def callback_request_version(self, origin, target):
        self.callbacks.append("Version")
    
    def callback_request_stats(self, origin, target, stat, arg):
        self.callbacks.append("Stats")
    
    def callback_trace(self, origin, search, target):
        self.callbacks.append("Trace")
    
    def callback_ping(self, origin, source, target):
        self.callbacks.append("Ping")
    
    def callback_pong(self, origin, source, target):
        self.callbacks.append("Pong")
    
    def callback_request_whois(self, origin, target, search):
        self.callbacks.append("Whois")
    
    def callback_privmsg(self, origin, target, message):
        self.callbacks.append("Privmsg")
    
    def callback_oobmsg(self, args):
        self.callbacks.append("Oobmsg")
    
    def callback_notice(self, origin, target, message):
        self.callbacks.append("Notice")
    
    def callback_wallops(self, origin, message):
        self.callbacks.append("Wallops")
    
    def callback_wallusers(self, origin, message):
        self.callbacks.append("Wallusers")
    
    def callback_wallvoices(self, origin, channel, message):
        self.callbacks.append("Wallvoices")
    
    def callback_wallchops(self, origin, channel, message):
        self.callbacks.append("Wallchops")

class StateTest(unittest.TestCase):
    """
    Unit tests for wish.irc.state
    """
    
    def _setup_callbacks(self, s):
        n = ConnectionDouble()
        s.register_callback(
            State.CALLBACK_NEWUSER, n.callback_new_user)
        s.register_callback(
            State.CALLBACK_CHANGENICK, n.callback_change_nick)
        s.register_callback(
            State.CALLBACK_NEWSERVER, n.callback_new_server)
        s.register_callback(
            State.CALLBACK_AUTHENTICATE, n.callback_authenticate)
        s.register_callback(
            State.CALLBACK_USERMODECHANGE, n.callback_change_user_mode)
        s.register_callback(
            State.CALLBACK_AWAY, n.callback_away)
        s.register_callback(
            State.CALLBACK_BACK, n.callback_back)
        s.register_callback(
            State.CALLBACK_CHANNELCREATE, n.callback_channel_create)
        s.register_callback(
            State.CALLBACK_CHANNELJOIN, n.callback_channel_join)
        s.register_callback(
            State.CALLBACK_CHANNELPART, n.callback_channel_part)
        s.register_callback(
            State.CALLBACK_CHANNELPARTALL, n.callback_part_all)
        s.register_callback(
            State.CALLBACK_CHANNELMODECHANGE, n.callback_channel_change_mode)
        s.register_callback(
            State.CALLBACK_CHANNELBANADD, n.callback_channel_add_ban)
        s.register_callback(
            State.CALLBACK_CHANNELBANREMOVE, n.callback_channel_remove_ban)
        s.register_callback(
            State.CALLBACK_CHANNELBANCLEAR, n.callback_channel_clear_bans)
        s.register_callback(
            State.CALLBACK_CHANNELOP, n.callback_channel_op)
        s.register_callback(
            State.CALLBACK_CHANNELDEOP, n.callback_channel_deop)
        s.register_callback(
            State.CALLBACK_CHANNELCLEAROPS, n.callback_channel_clear_ops)
        s.register_callback(
            State.CALLBACK_CHANNELVOICE, n.callback_channel_voice)
        s.register_callback(
            State.CALLBACK_CHANNELDEVOICE, n.callback_channel_devoice)
        s.register_callback(
            State.CALLBACK_CHANNELCLEARVOICES, n.callback_channel_clear_voices)
        s.register_callback(
            State.CALLBACK_GLINEADD, n.callback_gline_add)
        s.register_callback(
            State.CALLBACK_GLINEREMOVE, n.callback_gline_remove)
        s.register_callback(
            State.CALLBACK_INVITE, n.callback_invite)
        s.register_callback(
            State.CALLBACK_JUPEADD, n.callback_jupe_add)
        s.register_callback(
            State.CALLBACK_JUPEREMOVE, n.callback_jupe_remove)
        s.register_callback(
            State.CALLBACK_REQUESTADMIN, n.callback_admin_info)
        s.register_callback(
            State.CALLBACK_REQUESTINFO, n.callback_info_request)
        s.register_callback(
            State.CALLBACK_CHANNELKICK, n.callback_kick)
        s.register_callback(
            State.CALLBACK_CHANNELPARTZOMBIE, n.callback_zombie_part)
        s.register_callback(
            State.CALLBACK_CHANNELDESTROY, n.callback_channel_destroy)
        s.register_callback(
            State.CALLBACK_QUIT, n.callback_quit)
        s.register_callback(
            State.CALLBACK_KILL, n.callback_kill)
        s.register_callback(
            State.CALLBACK_REQUESTLUSERS, n.callback_lusers)
        s.register_callback(
            State.CALLBACK_REQUESTLINKS, n.callback_links)
        s.register_callback(
            State.CALLBACK_REQUESTMOTD, n.callback_motd)
        s.register_callback(
            State.CALLBACK_REQUESTNAMES, n.callback_names)
        s.register_callback(
            State.CALLBACK_CHANNELTOPIC, n.callback_topic)
        s.register_callback(
            State.CALLBACK_SILENCEADD, n.callback_silence_add)
        s.register_callback(
            State.CALLBACK_SILENCEREMOVE, n.callback_silence_remove)
        s.register_callback(
            State.CALLBACK_SERVERQUIT, n.callback_squit)
        s.register_callback(
            State.CALLBACK_REQUESTVERSION, n.callback_request_version)
        s.register_callback(
            State.CALLBACK_REQUESTSTATS, n.callback_request_stats)
        s.register_callback(
            State.CALLBACK_TRACE, n.callback_trace)
        s.register_callback(
            State.CALLBACK_PING, n.callback_ping)
        s.register_callback(
            State.CALLBACK_PONG, n.callback_pong)
        s.register_callback(
            State.CALLBACK_REQUESTWHOIS, n.callback_request_whois)
        s.register_callback(
            State.CALLBACK_PRIVMSG, n.callback_privmsg)
        s.register_callback(
            State.CALLBACK_OOBMSG, n.callback_oobmsg)
        s.register_callback(
            State.CALLBACK_NOTICE, n.callback_notice)
        s.register_callback(
            State.CALLBACK_WALLOPS, n.callback_wallops)
        s.register_callback(
            State.CALLBACK_WALLUSERS, n.callback_wallusers)
        s.register_callback(
            State.CALLBACK_WALLVOICES, n.callback_wallvoices)
        s.register_callback(
            State.CALLBACK_WALLCHOPS, n.callback_wallchops)
        return n
    
    def testAuthentication(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        s.authenticate((1, None), (1, 1), "Test")
        self.assertEqual("Test", s.get_account_name((1, 1)))
    
    def testcallback_authenticate(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.authenticate((1, None), (1, 1), "Test")
        self.assertEquals(["Authenticate"], n.callbacks)
    
    def testAuthenticationOnlyExistingUsers(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.authenticate, (1, None), (1, 1), "Test")
    
    def testAuthenticationOnlyOnce(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        s.authenticate((1, None), (1, 1), "Test")
        self.assertRaises(
            StateError, s.authenticate, (1, None), (1, 1), "Test2")
    
    def testAuthenticationSourceMustBeServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        self.assertRaises(ProtocolError, s.authenticate, (1, 1), (1, 1), "Test")
        
    def testOnlyValidServerCanAuthUsers(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.authenticate, (8, None), (1, 1), "Test")
    
    def testGetNumericID(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEqual(1, s.server_id)
    
    def testGetServerName(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEqual("example.com", s.server_name)
    
    def testGetServerDescription(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEqual("Example test", s.server_description)
    
    def testGetServerAdmin(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEqual("test", s.admin_name)    
    def testGetServerEmail(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEqual("test@example.com", s.contact_email)
    
    def testOnlyServerCanCreateUser(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(ProtocolError, s.new_user, (1, 6), (1, 1), "test",
                          "test", "example.com", [], 0, 0, 0, "Test User")
    
    def testCorrectModesOnCreation(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.users[(1, 1)].has_mode('o'))
        self.assertFalse(s.users[(1, 1)].has_mode('b'))
    
    def testCorrectModesWithArgs(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.users[(1, 1)].change_mode(("+b","test"))
        self.assertEquals(s.users[(1, 1)].has_mode('b'), "test")
    
    def testNegativeModesWithArgs(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+b", None)], 0, 0, 0, "Test User")
        s.users[(1, 1)].change_mode(("-b",None))
        self.assertFalse(s.users[(1, 1)].has_mode('b'))
    
    def testnew_userMustNotExist(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.new_user, (1, None), (1, 1),
                          "test2", "test2", "example.com", [("+r", "Test")],
                          6, 0, 0, "Duplicate Test User")
    
    def testnew_userAuthenticatesCorrectly(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+r", "test")], 0, 0, 0, "Test User")
        self.assertEquals("test", s.users[(1, 1)].account)
    
    def testChangeNick(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.change_nick((1, 1), (1, 1), "test2", 2)
        self.assertEquals(s.users[(1, 1)].nickname, "test2")
    
    def testChangeNickUnknownUser(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.change_nick, (1,None), (1, 1),
                          "test2", 2)
    
    def testMarkAway(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1, 1)].is_away())
        s.set_away((1, 1), "Away reason")
        self.assertTrue(s.users[(1, 1)].is_away())
    
    def testMarkAwayCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.set_away((1, 1), "Away reason")
        self.assertEquals(["Away"], n.callbacks)
    
    def testMarkAwayNeedsParam(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.set_away, (1, 1), "")
    
    def testMarkAwayNeedsExist(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.set_away, (1, 1), "")
    
    def testMarkBack(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1, 1)].is_away())
        s.set_away((1, 1), "Away reason")
        self.assertTrue(s.users[(1, 1)].is_away())
        s.set_back((1, 1))
        self.assertFalse(s.users[(1, 1)].is_away())
    
    def testMarkBackCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.set_back((1, 1))
        self.assertEquals(["Back"], n.callbacks)
    
    def testMarkBackNeedsExist(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.set_back, (1, 1))
    
    def testCreateChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.create_channel((1, 1), "#test", 6))
        self.assertTrue(s.channel_exists("#test"))
        self.assertFalse(s.channel_exists("#example"))
    
    def testCreateChannelServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.create_channel((1, None), "#test", 6))
        self.assertTrue(s.channel_exists("#test"))
    
    def testCreateChannelCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.create_channel((1, 1), "#test", 6)
        self.assertEquals(["ChannelCreate"], n.callbacks)
    
    def testCreateChannelClashBothOp(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,8), "test2", "test2", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.create_channel((1, 1), "#test", 6))
        self.assertTrue(s.create_channel((1,8), "#test", 6))
        self.assertTrue(s.channel_exists("#test"))
        self.assertTrue(s.channels["#test"].isop((1, 1)))
        self.assertTrue(s.channels["#test"].isop((1,8)))
    
    def testCreateChannelEqualTSClashCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,8), "test2", "test2", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        n = self._setup_callbacks(s)
        s.create_channel((1, 1), "#test", 6)
        s.create_channel((1,8), "#test", 6)
        self.assertEquals(["ChannelCreate", "ChannelJoin", "Op"], n.callbacks)
    
    def testCreateChannelUserJoinsIt(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.create_channel((1, 1), "#test", 6))
        self.assertTrue(s.channel_exists("#test"))
        self.assertTrue(s.channels["#test"].isop((1, 1)))
    
    def testCreateChannelMustBeValidUser(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.create_channel, (1, 1), "#test", 6)
        self.assertFalse(s.channel_exists("#test"))
    
    def testChannelJoinerMustExist(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.join_channel, (1,8), (1,8), "#test", [])
    
    def testReplaceChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.create_channel((1, 1), "#test", 6))
        self.assertTrue(s.channels["#test"].isop((1, 1)))
        self.assertTrue(s.create_channel((1, 2), "#test", 3))
        self.assertEquals(3, s.channels["#test"].ts)
        self.assertFalse(s.channels["#test"].isop((1, 1)))
        self.assertTrue(s.channels["#test"].isop((1,2)))
        self.assertFalse(s.create_channel((1, 1), "#test", 6))
    
    def testCreateChannelOverridesCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,8), "test2", "test2", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        n = self._setup_callbacks(s)
        s.create_channel((1, 1), "#test", 6)
        s.create_channel((1,8), "#test", 3)
        self.assertEquals(
            ["ChannelCreate", "ClearOps", "ClearVoices", "ClearBans",
             "ChannelJoin", "Op"],
            n.callbacks)
    
    def testSetChannelModes(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].has_mode("p"))
        s.change_channel_mode((1, 1), "#test", [("+p", None)])
        self.assertTrue(s.channels["#test"].has_mode("p"))
    
    def testSetChannelModesMulti(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].has_mode("p"))
        self.assertFalse(s.channels["#test"].has_mode("k"))
        s.change_channel_mode((1, 1), "#test", [("+p", None),("+k", "Test")])
        self.assertTrue(s.channels["#test"].has_mode("p"))
        self.assertEquals("Test", s.channels["#test"].has_mode("k"))
    
    def testSetChannelModesCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.change_channel_mode((1, 1), "#test", [("+p", None)])
        self.assertEquals(["ChannelChangeMode"], n.callbacks)
    
    def testSetChannelModesWithArgs(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].has_mode("l"))
        s.change_channel_mode((1, 1), "#test", [("+l", "26")])
        self.assertEquals("26", s.channels["#test"].has_mode("l"))
    
    def testChannelModeChangerMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.change_channel_mode, (1,8),
                          "#test", ("+l", "26"))
        self.assertRaises(StateError, s.change_channel_mode, (4, None),
                          "#test", ("+l", "26"))
    
    def testAddChannelBan(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertTrue("*!*@*.example.com" in s.channels["#test"].bans)
    
    def testAddChannelBanCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["BanAdd"], n.callbacks)
    
    def testAddChannelBanNonExistantChannel(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(
            StateError,
            s.add_channel_ban,(1,None), "#test", "*!*@*.example.com")
    
    def testChannelBannerMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(
            StateError,
            s.add_channel_ban, (1,8), "#test", "*!*@*.example.com")
        self.assertRaises(
            StateError,
            s.add_channel_ban, (4, None), "#test", "*!*@*.example.com")
        
    def testJoinNonExistentChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.join_channel((1, 1), (1, 1), "#test", "o")
        self.assertTrue(s.channel_exists("#test"))
        self.assertTrue((1, 1) in s.channels["#test"].users)
        self.assertTrue(s.channels["#test"].isop((1, 1)))
    
    def testJoinCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,8), "test2", "test2", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.join_channel((1,8), (1,8), "#test", [])
        self.assertEquals(["ChannelJoin"], n.callbacks)
    
    def testJoinButReallyCreateCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.join_channel((1, 1), (1, 1), "#test", "o")
        self.assertEquals(["ChannelCreate"], n.callbacks)
    
    def testChangeModeNonExistantChannel(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.change_channel_mode, (1, 1),
                          "#test", ("+o", None))
    
    def testUnban(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.remove_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testUnbanCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        n = self._setup_callbacks(s)
        s.remove_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["BanRemove"], n.callbacks)
    
    def testUnbanMask(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.remove_channel_ban((1, 1), "#test", "*!*@*.com")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testUnbanBadMask(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.remove_channel_ban((1, 1), "#test", "*!*@notanexample.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
    
    def testUnbanBadChan(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(
            StateError,
            s.remove_channel_ban, (1, 1), "#test", ["*!*@*.example.com"])
    
    def testClearBans(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        s.clear_channel_bans((1, 1), "#test")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testClearBansCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.add_channel_ban((1, 1), "#test", "*!*@*.example.com")
        n = self._setup_callbacks(s)
        s.clear_channel_bans((1, 1), "#test")
        self.assertEquals(['ClearBans'], n.callbacks)
    
    def testClearBansBadChan(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.clear_channel_bans,(1, 1), "#test")
    
    def testChannelBanRemoverMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(
            StateError,
            s.remove_channel_ban, (1,8), "#test", "*!*@*.example.com")
        self.assertRaises(
            StateError,
            s.remove_channel_ban, (4, None), "#test", "*!*@*.example.com")
    
    def testChannelBanClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.clear_channel_bans, (1,8), "#test")
        self.assertRaises(StateError, s.clear_channel_bans, (4, None), "#test")
    
    def testClearOps(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertEquals(set([(1, 1)]), s.channels["#test"].ops)
        s.clear_channel_ops((1, 1), "#test")
        self.assertEquals(set([]), s.channels["#test"].ops)
    
    def testClearOpsCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.clear_channel_ops((1, 1), "#test")
        self.assertEquals(['ClearOps'], n.callbacks)
    
    def testChannelOpClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.clear_channel_ops, (1,8), "#test")
        self.assertRaises(StateError, s.clear_channel_ops, (4, None), "#test")
    
    def testClearOpsBadChan(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.clear_channel_ops, (1, 1), "#test")
    
    def testDeopBadChan(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.deop, (1, 1), "#test", (1, 1))
    
    def testOp(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        self.assertFalse(s.channels["#test"].isop((1,2)))
        s.op((1, 1), "#test", (1,2))
        self.assertTrue(s.channels["#test"].isop((1,2)))
    
    def testOpCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        n = self._setup_callbacks(s)
        s.op((1, 1), "#test", (1,2))
        self.assertEquals(['Op'], n.callbacks)
    
    def testOpBadUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.op, (1, 1), "#test", (1,6))
    
    def testOpBadChan(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1,None),(1,6), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.op, (1, 1), "#test", (1,6))
    
    def testDeopCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", ["o"])
        n = self._setup_callbacks(s)
        s.deop((1, 1), "#test", (1,2))
        self.assertEquals(['Deop'], n.callbacks)
    
    def testDeopBadUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.deop, (1, 1), "#test", (1,6))
    
    def testClearVoices(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1, 1), (1, 1), "#test", ["v"])
        self.assertEquals(set([(1, 1)]), s.channels["#test"].voices)
        s.clear_channel_voices((1, 1), "#test")
        self.assertEquals(set([]), s.channels["#test"].voices)
    
    def testClearVoicesCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", ["v"])
        n = self._setup_callbacks(s)
        s.clear_channel_voices((1, 1), "#test")
        self.assertEquals(['ClearVoices'], n.callbacks)
    
    def testChannelVoiceClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(
            StateError, s.clear_channel_voices, (1,8), "#test")
        self.assertRaises(
            StateError, s.clear_channel_voices, (4, None), "#test")
    
    def testClearVoicesBadChan(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.clear_channel_voices, (1, 1), "#test")
    
    def testDevoiceBadChan(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.devoice, (1, 1), "#test", (1, 1))
    
    def testDevoiceBadUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.devoice, (1, 1), "#test", (1, 1))
    
    def testDevoiceCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", ["v"])
        n = self._setup_callbacks(s)
        s.devoice((1, 1), "#test", (1,2))
        self.assertEquals(['Devoice'], n.callbacks)
    
    def testVoice(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].isvoice((1,2)))
        s.join_channel((1,2), (1,2), "#test", [])
        self.assertFalse(s.channels["#test"].isvoice((1,2)))
        s.voice((1, 1), "#test", (1,2))
        self.assertTrue(s.channels["#test"].isvoice((1,2)))
    
    def testVoiceCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        n = self._setup_callbacks(s)
        s.voice((1, 1), "#test", (1,2))
        self.assertEquals(['Voice'], n.callbacks)
    
    def testVoiceBadUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.voice, (1, 1), "#test", (1,6))
    
    def testVoiceBadChan(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1,None),(1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1,None),(1,6), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.voice, (1, 1), "#test", (1,6))
    
    def testNewServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        self.assertTrue(s.server_exists(2))
        self.assertEquals(1000, s.max_client_numerics[2])
    
    def testNoDuplicateServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        self.assertRaises(
            StateError,
            s.new_server, (1, None), 2, "test.example.org", 1000, 0, 0, "P10",
            1, "", "A testing server")
    
    def testOnlyServerCanIntroduceServer(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(
            ProtocolError,
            s.new_server, (1, 8), 2, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
    
    def testOnlyExistingServerCanIntroduceServer(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(
            StateError,
            s.new_server, (177, None), 2, "test.example.org", 1000, 0, 0,
            "P10", 1, "", "A testing server")
    
    def testCurrentServerAlwaysExists(self):
        c = ConfigDouble()
        s = State(c)
        self.assertTrue(s.server_exists(1))
    
    def testOnlyValidServerCanCreateUsers(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(
            StateError,
            s.new_user, (8, None), (1, 1), "test", "test", "example.com",
            [("+b", None)], 0, 0, 0, "Test User")
    
    def testAddGline(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
    
    def testAddGlineCallback(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        self.assertEquals(["GlineAdd"], n.callbacks)
    
    def testIsGlinedMaskCheck(self):
        c = ConfigDouble()
        s = State(c)
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("test!foo@bar.com"))
    
    def testGlinesExpire(self):
        c = ConfigDouble()
        s = State(c)
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts - 3600, 6, "A test g-line")
        self.assertFalse(s.is_glined("test!foo@bar.com"))
    
    def testRemoveGline(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
        s.remove_gline((1, 1), "*!foo@bar.com", None, 6)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
    
    def testRemoveGlineCallback(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        n = self._setup_callbacks(s)
        s.remove_gline((1, 1), "*!foo@bar.com", None, 6)
        self.assertEquals(["GlineRemove"], n.callbacks)
    
    def testRemoveGlineMask(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline(
            (1, 1), "*!foo@bar.com", None, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
        s.remove_gline((1, 1), "*!*@bar.com", None, 6)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
    
    def testAddGlineSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline((1, 1), "*!foo@bar.com", 1, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
    
    def testAddGlineNotSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline((1, 1), "*!foo@bar.com", 8, s.ts + 3600, 6, "A test g-line")
        self.assertFalse(s.is_glined("*!foo@bar.com"))
    
    def testRemoveGlineSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline((1, 1), "*!foo@bar.com", 1, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
        s.remove_gline((1, 1), "*!foo@bar.com", 1, 6)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
    
    def testRemoveGlineNotSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_glined("*!foo@bar.com"))
        s.add_gline((1, 1), "*!foo@bar.com", 1, s.ts + 3600, 6, "A test g-line")
        self.assertTrue(s.is_glined("*!foo@bar.com"))
        s.remove_gline((1, 1), "*!foo@bar.com", 8, 6)
        self.assertTrue(s.is_glined("*!foo@bar.com"))
    
    def testGetGlobalGlines(self):
        c = ConfigDouble()
        s = State(c)
        expires = s.ts + 3600
        s.add_gline(
            (1, 1), "*!foo@bar.com", 1, expires, 6, "A local test g-line")
        s.add_gline(
            (1, 1), "*!foo2@bar.com", None, expires, 6, "A global test g-line")
        s.add_gline(
            (1, 1), "*!foo3@bar.com", None, expires, 6,
            "A global deactivated g-line")
        s.remove_gline((1, 1), "*!foo3@bar.com", None, 6)
        self.assertEquals(2, len(s.glines))
        self.assertTrue(
            ("*!foo2@bar.com", "A global test g-line", expires, True, 6)
                in s.glines)
        self.assertTrue(
            ("*!foo3@bar.com", "A global deactivated g-line", expires, False, 6)
                in s.glines)
    
    def testPartChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        self.assertTrue(s.channels["#test"].ison((1, 1)))
        s.part_channel((1, 1), "#test", "Test")
        self.assertFalse(s.channels["#test"].ison((1, 1)))
    
    def testUnknownUserPartsChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.part_channel, (1,8), "#test", "Test")
    
    def testUserNotOnChannelPartsChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.part_channel, (1,2), "#test", "Test")
    
    def testPartingChannelMustExist(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.part_channel, (1, 1), "#test", "Test")
    
    def testLastUserToPartsTurnsLightsOff(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        s.part_channel((1, 1), "#test", "Test")
        s.part_channel((1,2), "#test", "Test")
        self.assertFalse(s.channel_exists("#test"))
    
    def testUserPartsAllChannels(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        self.assertTrue(s.channels["#test"].ison((1, 1)))
        s.part_all_channels((1, 1))
        self.assertFalse(s.channels["#test"].ison((1, 1)))
    
    def testInvite(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.invite((1, 1), (1,2), "#test")
        self.assertTrue(s.users[(1,2)].is_invited("#test"))
    
    def testInviteCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.invite((1, 1), (1,2), "#test")
        self.assertEquals(["Invite"], n.callbacks)
    
    def testInvitesAreHandedInOnJoin(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.invite((1, 1), (1,2), "#test")
        s.join_channel((1,2), (1,2), "#test", [])
        self.assertFalse(s.users[(1,2)].is_invited("#test"))
    
    def testChannelRemovalRemovesInvites(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        s.invite((1, 1), (1,2), "#test")
        s.part_channel((1, 1), "#test", "Test")
        self.assertFalse(s.users[(1,2)].is_invited("#test"))
    
    def testGetNumericFromNick(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        self.assertEquals((1, 1), s.nick2numeric("test"))
        self.assertEquals((1,2), s.nick2numeric("test2"))
        self.assertEquals(None, s.nick2numeric("foo"))
    
    def testGetNumericFromServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 0, "P10",
            1, "", "A testing server")
        self.assertEquals((1,None), s.nick2numeric("example.com"))
        self.assertEquals((2,None), s.nick2numeric("test.example.org"))
        self.assertEquals(None, s.nick2numeric("foo.example.com"))
    
    def testInviteTargetMustExist(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.invite, (1, 1), (1,8), "#test")
    
    def testInviteChannelMustExist(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,8), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertRaises(StateError, s.invite, (1, 1), (1,8), "#test")
    
    def testcallback_new_user(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertEquals(["new_user"], n.callbacks)
    
    def testCallbacksCanBeMultiple(self):
        c = ConfigDouble()
        s = State(c)
        n1 = self._setup_callbacks(s)
        n2 = self._setup_callbacks(s)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertEquals(["new_user"], n1.callbacks)
        self.assertEquals(["new_user"], n2.callbacks)
    
    def testcallback_change_nick(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.change_nick((1, 1), (1, 1), "test2", 16000)
        self.assertEquals(["ChangeNick"], n.callbacks)
    
    def testcallback_new_server(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        self.assertEquals(["NewServer"], n.callbacks)
    
    def testPartChannelCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.part_channel((1, 1), "#test", "Test")
        self.assertEquals(["ChannelPart"], n.callbacks)
    
    def testPartAllChannelCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test2", "example.com",
            [("+l", None)], 0, 0, 0, "Test User 2")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.part_all_channels((1, 1))
        self.assertEquals(["PartAll"], n.callbacks)
    
    def testAddJupe(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        self.assertTrue(s.is_juped("test.example.com"))
    
    def testAddJupeCallback(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        self.assertEquals(["JupeAdd"], n.callbacks)
    
    def testJupesExpire(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts - 3600, 6, "Testing")
        self.assertFalse(s.is_juped("test.example.com"))
    
    def testAddJupeSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", 1, s.ts + 3600, 6, "Testing")
        self.assertTrue(s.is_juped("test.example.com"))
    
    def testAddJupeSpecificTargetButNotUs(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", 18, s.ts + 3600, 6, "Testing")
        self.assertFalse(s.is_juped("test.example.com"))
    
    def testRemoveJupe(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        self.assertTrue(s.is_juped("test.example.com"))
        s.remove_jupe((1, 1), "test.example.com", None, 6)
        self.assertFalse(s.is_juped("test.example.com"))
    
    def testRemoveJupeCallback(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        n = self._setup_callbacks(s)
        s.remove_jupe((1, 1), "test.example.com", None, 6)
        self.assertEquals(["JupeRemove"], n.callbacks)
    
    def testRemoveJupeSpecificTarget(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        s.remove_jupe((1, 1), "test.example.com", 1, 6)
        self.assertFalse(s.is_juped("test.example.com"))
    
    def testRemoveJupeSpecificTargetButNotUs(self):
        c = ConfigDouble()
        s = State(c)
        self.assertFalse(s.is_juped("test.example.com"))
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.add_jupe((1, 1), "test.example.com", None, s.ts + 3600, 6, "Testing")
        s.remove_jupe((1, 1), "test.example.com", 7, 6)
        self.assertTrue(s.is_juped("test.example.com"))
    
    def testGetGlobalJupes(self):
        c = ConfigDouble()
        s = State(c)
        expires = s.ts + 3600
        s.add_jupe((1, 1), "test.example.com", 1, expires, 6, "Local jupe")
        s.add_jupe(
            (1, 1), "test2.example.com", None, expires, 6, "A global test jupe")
        s.add_jupe((1, 1), "test3.example.com", None, expires, 6,
            "A global deactivated jupe")
        s.remove_jupe((1, 1), "test3.example.com", None, 6)
        self.assertEquals(2, len(s.jupes))
        self.assertTrue(
            ("test2.example.com", "A global test jupe", expires, True, 6)
                in s.jupes)
        self.assertTrue(
            ("test3.example.com", "A global deactivated jupe", expires, False,
             6) in s.jupes)
    
    def testSendAdminCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_admininfo((1, 1), (1, None))
        self.assertEquals(["RequestAdmin"], n.callbacks)
    
    def testSendAdminCallbackOnlyIfOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_admininfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendAdminTargetMustBeServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(ProtocolError, s.request_admininfo, (1, 1), (1, 1))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoCallback(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_serverinfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoCallbackOnlyIfOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_serverinfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoTargetMustBeServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(ProtocolError, s.request_serverinfo, (1, 1), (1, 1))
        self.assertEquals([], n.callbacks)
    
    def testKickLocalUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((1,2), (1,2), "#test", [])
        n = self._setup_callbacks(s)
        s.kick((1, 1), "#test", (1,2), "Testing")
        self.assertFalse(s.channels["#test"].ison((1,2)))
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickRemoteUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_server((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        s.new_user((6, None), (6,2), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        s.join_channel((6,2), (6,2), "#test", [])
        n = self._setup_callbacks(s)
        s.kick((1, 1), "#test", (6,2), "Testing")
        self.assertTrue(s.channels["#test"].ison((6,2)))
        self.assertFalse((6,2) in s.channels["#test"].users)
        self.assertEquals(["ChannelKick"], n.callbacks)
        s.part_channel((6,2), "#test", "bouncing kick")
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickOnInvalidChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(StateError, s.kick, (1, 1), "#test", (1,2), "Testing")
    
    def testKickOnInvalidUser(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertRaises(StateError, s.kick, (1, 1), "#test", (1,2), "Testing")
    
    def testKickingLastUserClosesChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        n = self._setup_callbacks(s)
        s.kick((1, 1), "#test", (1, 1), "Testing")
        self.assertFalse(s.channel_exists("#test"))
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickingLastUserRemoteDoesNotCloseChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        s.new_user((6, None), (6,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        s.create_channel((6,2), "#test", 6)
        n = self._setup_callbacks(s)
        s.kick((6, None), "#test", (6,2), "Testing")
        self.assertTrue(s.channel_exists("#test"))
        self.assertEquals(["ChannelKick"], n.callbacks)
        s.part_channel((6,2), "#test", "bouncing kick")
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
        self.assertFalse(s.channel_exists("#test"))
    
    def testDestructChannelIgnoresFullChannels(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 6)
        self.assertTrue(s.channel_exists("#test"))
        n = self._setup_callbacks(s)
        s.destroy_channel((1, None), "#test", 6)
        self.assertEquals([], n.callbacks)
        self.assertTrue(s.channel_exists("#test"))
    
    def testDestructChannelIgnoresBadChannels(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.destroy_channel((1, None), "#test", 6)
        self.assertEquals(['DestroyChannel'], n.callbacks)
        self.assertFalse(s.channel_exists("#test"))
    
    def testDestructChannelRemovesZombifiedChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1,
            "", "A testing server")
        s.new_user((6, None), (6,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        s.create_channel((6,2), "#test", 6)
        s.kick((6, None), "#test", (6,2), "Testing")
        self.assertTrue(s.channel_exists("#test"))
        n = self._setup_callbacks(s)
        s.destroy_channel((6, None), "#test", 6)
        self.assertEquals(['DestroyChannel'], n.callbacks)
        self.assertFalse(s.channel_exists("#test"))
    
    def testUserQuit(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.user_exists((1, 1)))
        s.quit((1, 1), "A reason")
        self.assertFalse(s.user_exists((1, 1)))
    
    def testUserQuitCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.quit((1, 1), "A reason")
        self.assertEquals([('Quit', 'A reason')], n.callbacks)
    
    def testUserQuitMustExist(self):
        c = ConfigDouble()
        s = State(c)
        self.assertRaises(StateError, s.quit, (1, 1), "A reason")
    
    def testUserQuittingLeavesChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 16)
        s.join_channel((1,2), (1,2), "#test", [])
        s.quit((1,2), "A reason")
        self.assertFalse(s.channels["#test"].ison((1,2)))
    
    def testLastUserQuittingClosesChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 16)
        s.quit((1, 1), "A reason")
        self.assertFalse(s.channel_exists("#test"))
    
    def testUserKillLocal(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 3, "origin.example.com", 1000, 0, 0, "P10",
            1, "", "A testing server")
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.user_exists((1, 1)))
        n = self._setup_callbacks(s)
        s.kill((3,None), (1, 1), [], "Testing")
        self.assertFalse(s.user_exists((1, 1)))
        self.assertEquals([("Quit", "Killed (Testing)")], n.callbacks)
    
    def testUserKillRemote(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 3, "origin.example.com", 1000, 0, 0, "P10",
            1, "", "A testing server")
        s.new_server((1, None), 6, "test.example.org", 1000, 0, 0, "P10",
            1, "", "A testing server")
        s.new_user((6, None), (6,2), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.user_exists((6,2)))
        n = self._setup_callbacks(s)
        s.kill((3,None), (6,2), [], "Testing")
        self.assertTrue(s.user_exists((6,2)))
        self.assertEquals(
            [("Kill", ["origin.example.com"], "Testing")],
            n.callbacks)
    
    def testSendLinksCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_links((1, 1), (1, None), "*.example.com")
        self.assertEquals(["Links"], n.callbacks)
    
    def testSendLinksCallbackOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.request_links, (1, 1), (1, None), "*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSendLinksCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(
            ProtocolError, s.request_links,(1, 1), (1, 6), "*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSendLusersCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_lusers((1, 1), (1, None), "Dummy")
        self.assertEquals(["Lusers"], n.callbacks)
    
    def testSendLusersCallbackOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.request_lusers, (1, 1), (1, None), "dummy")
        self.assertEquals([], n.callbacks)
    
    def testSendLusersCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(
            ProtocolError, s.request_lusers, (1, 1), (1, 6), "dummy")
        self.assertEquals([], n.callbacks)
    
    def testSendMOTDCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_motd((1, 1), (1, None))
        self.assertEquals(["MOTD"], n.callbacks)
    
    def testSendMOTDCallbackOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_motd, (1, 1), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendMOTDCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(ProtocolError, s.request_motd, (1, 1), (1, 6))
        self.assertEquals([], n.callbacks)
    
    def testChangeUserMode(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com", [],
            0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.change_user_mode((1, 1), [("+o", None)])
        self.assertTrue(s.users[(1, 1)].has_mode("o"))
        self.assertEquals(['ChangeUserMode'], n.callbacks)
    
    def testChangeUserModeMultiple(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com", [],
            0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.change_user_mode((1, 1), [("+o", None),("+h", "Test")])
        self.assertTrue(s.users[(1, 1)].has_mode("o"))
        self.assertEquals("Test", s.users[(1, 1)].has_mode("h"))
        self.assertEquals(['ChangeUserMode'], n.callbacks)
    
    def testChangeUserModeMustExist(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError,
            s.change_user_mode, (1, 1), [("+o", None),("+h", "Test")])
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallback(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        s.request_channel_users((1, 1), (1, None), ["#test"])
        self.assertEquals(["Names"], n.callbacks)
    
    def testSendNamesCallbackOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.request_channel_users, (1,6), (1, None), ["#test"])
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        self.assertRaises(
            ProtocolError, s.request_channel_users, (1, 1), (1, 6), ["#test"])
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallbackChannelisChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_channel_users((1, 1), (1, None), ["#test"])
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallbackNotIfChannelIsP(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        s.channels["#test"].change_mode(("+p", None))
        n = self._setup_callbacks(s)
        s.request_channel_users((1,2), (1, None), ["#test"])
        self.assertEquals([], n.callbacks)
        s.request_channel_users((1, 1), (1, None), ["#test"])
        self.assertEquals(["Names"], n.callbacks)
    
    def testSendNamesCallbackNotIfChannelIsS(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((1, None), (1,2), "test2", "test", "example.com",
            [], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        s.channels["#test"].change_mode(("+p", None))
        n = self._setup_callbacks(s)
        s.request_channel_users((1,2), (1, None), ["#test"])
        self.assertEquals([], n.callbacks)
        s.request_channel_users((1, 1), (1, None), ["#test"])
        self.assertEquals(["Names"], n.callbacks)
    
    def testNumeric2Nick(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        self.assertEquals("test", s.numeric2nick((1, 1)))
    
    def testSelfServerNumeric2Nick(self):
        c = ConfigDouble()
        s = State(c)
        self.assertEquals("example.com", s.numeric2nick((1,None)))
    
    def testServerNumeric2Nick(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 0,
            "P10", 1, "", "A testing server")
        self.assertEquals("test.example.org", s.numeric2nick((2, None)))
    
    def testChangeTopic(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        self.assertEquals("", s.channels["#test"].topic)
        s.change_topic((1, 1), "#test", "New topic", 19, 18)
        self.assertEquals("New topic", s.channels["#test"].topic)
        self.assertEquals("test", s.channels["#test"].topic_changer)
        self.assertEquals(19, s.channels["#test"].topic_ts)
        self.assertEquals(["Topic"], n.callbacks)
    
    def testChangeTopicOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.change_topic, (1, 1), "#test",
                          "New topic", 19, 18)
        self.assertEquals([], n.callbacks)
    
    def testChangeTopicchannel_exists(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.change_topic, (1, 1), "#test",
                          "New topic", 19, 18)
        self.assertEquals([], n.callbacks)
    
    def testChangeTopicDisregardOlderMessages(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        self.assertEquals("", s.channels["#test"].topic)
        s.change_topic((1, 1), "#test", "New topic", 162, 18)
        s.change_topic((1, 1), "#test", "Old topic", 19, 18)
        self.assertEquals("New topic", s.channels["#test"].topic)
        self.assertEquals("test", s.channels["#test"].topic_changer)
        self.assertEquals(162, s.channels["#test"].topic_ts)
        self.assertEquals(["Topic"], n.callbacks)
    
    def testChangeTopicDisregardMessagesForNewerChannel(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((1, 1), "#test", 18)
        n = self._setup_callbacks(s)
        self.assertEquals("", s.channels["#test"].topic)
        s.change_topic((1, 1), "#test", "New topic", 19, 18)
        s.change_topic((1, 1), "#test", "Topic for younger channel", 162, 38)
        self.assertEquals("New topic", s.channels["#test"].topic)
        self.assertEquals("test", s.channels["#test"].topic_changer)
        self.assertEquals(19, s.channels["#test"].topic_ts)
        self.assertEquals(["Topic"], n.callbacks)
    
    def testSilenceAdd(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertFalse(s.users[(1, 1)].is_silenced("test!foo@bar.example.com"))
        s.add_silence((1, 1), "*!*@*.example.com")
        self.assertTrue(s.users[(1, 1)].is_silenced("test!foo@bar.example.com"))
        self.assertEquals(["SilenceAdd"], n.callbacks)
    
    def testSilenceAddExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.add_silence, (1, 1), "*!*@*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSilenceRemove(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.remove_silence((1, 1), "*!*@*.example.com")
        self.assertFalse(s.users[(1, 1)].is_silenced("test!foo@bar.example.com"))
        n = self._setup_callbacks(s)
        s.add_silence((1, 1), "*!*@*.example.com")
        self.assertTrue(s.users[(1, 1)].is_silenced("test!foo@bar.example.com"))
        s.remove_silence((1, 1), "*!*@*.example.com")
        self.assertFalse(s.users[(1, 1)].is_silenced("test!foo@bar.example.com"))
        self.assertEquals(["SilenceAdd", "SilenceRemove"], n.callbacks)
    
    def testSilenceRemoveExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.remove_silence, (1, 1), "*!*@*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSquitRemoveServer(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        n = self._setup_callbacks(s)
        self.assertTrue(s.server_exists(2))
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.server_exists(2))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitIgnoreOlderTS(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        n = self._setup_callbacks(s)
        self.assertTrue(s.server_exists(2))
        s.quit_server((1, None), (2, None), "Test squit", 16)
        self.assertTrue(s.server_exists(2))
        s.quit_server((1, None), (2, None), "Test squit", 0)
        self.assertFalse(s.server_exists(2))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitRemoveServerExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.quit_server, (1, None), (2, None), "Test squit", 24)
        self.assertEquals([], n.callbacks)
    
    def testSquitRemoveChildServers(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((2, None), 3, "test2.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((3, None), 4, "test3.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        n = self._setup_callbacks(s)
        self.assertTrue(s.server_exists(2))
        self.assertTrue(s.server_exists(3))
        self.assertTrue(s.server_exists(4))
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.server_exists(2))
        self.assertFalse(s.server_exists(3))
        self.assertFalse(s.server_exists(4))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitRemoveGrandChildServers(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((2, None), 3, "test2.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        n = self._setup_callbacks(s)
        self.assertTrue(s.server_exists(2))
        self.assertTrue(s.server_exists(3))
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.server_exists(2))
        self.assertFalse(s.server_exists(3))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitRemoveUsers(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((2, None), 3, "test2.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_user((2, None), (2,1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((3, None), (3,1), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.user_exists((2,1)))
        self.assertFalse(s.user_exists((3,1)))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitRemoveEmptyChannels(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((2, None), 3, "test2.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_user((2, None), (2,1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((3, None), (3,1), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((2,1), "#test", 6)
        n = self._setup_callbacks(s)
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.user_exists((2,1)))
        self.assertFalse(s.user_exists((3,1)))
        self.assertFalse(s.channel_exists("#test"))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testSquitNoRemoveNonEmptyChannels(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_server((2, None), 3, "test2.example.org", 1000, 0, 24, "P10", 1,
            "", "A testing server")
        s.new_user((1, None), (1, 1), "test3", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((2, None), (2,1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.new_user((3, None), (3,1), "test2", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        s.create_channel((2,1), "#test", 6)
        s.join_channel((1, 1), (1, 1), "#test", [])
        n = self._setup_callbacks(s)
        s.quit_server((1, None), (2, None), "Test squit", 24)
        self.assertFalse(s.user_exists((2,1)))
        self.assertFalse(s.user_exists((3,1)))
        self.assertTrue(s.channel_exists("#test"))
        self.assertEquals(["Squit"], n.callbacks)
    
    def testVersion(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_version((1, 1), (1, None))
        self.assertEquals(["Version"], n.callbacks)
    
    def testVersionBadTarget(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(ProtocolError, s.request_version, (1, 1), (2, None))
        self.assertEquals([], n.callbacks)
    
    def testVersionBadOrigin(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_version, (1, 1), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testRequestStats(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_stats((1, 1), (1, None), "B", "test.example.com")
        self.assertEquals(["Stats"], n.callbacks)
    
    def testRequestStatsBadTarget(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(
            ProtocolError,
            s.request_stats, (1, 1), (2, None), "B", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testRequestStatsBadOrigin(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError,
            s.request_stats, (1, 1), (1, None), "B", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testRequestTrace(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.trace((1, 1), "test", (1, None))
        self.assertEquals(["Trace"], n.callbacks)
    
    def testRequestTraceBadTarget(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [("+o", None)], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        self.assertRaises(ProtocolError, s.trace, (1, 1), "test", (3, None))
        self.assertEquals([], n.callbacks)
    
    def testRequestTraceBadOrigin(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.trace, (1, 1), "test", (1, None))
        self.assertEquals([], n.callbacks)
    
    def testRegisterPing(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.register_ping((1, None), "AB", "test.example.com")
        self.assertEquals(["Ping"], n.callbacks)
    
    def testRegisterPingNonServer(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.register_ping, (7, None), "AB", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testRegisterPingUser(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.register_ping, (1, 8), "AB", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testRegisterPong(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.register_pong((1, None), "AB", "test.example.com")
        self.assertEquals(["Pong"], n.callbacks)
    
    def testRegisterPongNonServer(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.register_pong, (7, None), "AB", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testRegisterPongUser(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.register_pong, (1, 8), "AB", "test.example.com")
        self.assertEquals([], n.callbacks)
    
    def testWhois(self):
        c = ConfigDouble()
        s = State(c)
        s.new_user((1, None), (1, 1), "test", "test", "example.com",
            [], 0, 0, 0, "Test User")
        n = self._setup_callbacks(s)
        s.request_whois((1, 1), (1, None), "test")
        self.assertEquals(["Whois"], n.callbacks)
    
    def testWhoisOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.request_whois, (1, 1), (1, None), "test")
        self.assertEquals([], n.callbacks)
    
    def testWhoisTargetExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.request_whois, (1, 1), (6, None), "test")
        self.assertEquals([], n.callbacks)
    
    def testWhoisTargetIsServer(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.request_whois, (1, 1), (5,4), "test")
        self.assertEquals([], n.callbacks)
    
    def testPrivmsg(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.privmsg((1, None), "#test", "Test message")
        self.assertEquals(["Privmsg"], n.callbacks)
    
    def testPrivmsgOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.privmsg, (1, 7), "#test", "Test message")
        self.assertEquals([], n.callbacks)
    
    def testNotice(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.notice((1, None), "#test", "Test message")
        self.assertEquals(["Notice"], n.callbacks)
    
    def testNoticeOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.notice, (1, 7), "#test", "Test message")
        self.assertEquals([], n.callbacks)
    
    def testWallvoices(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.wallvoices((1, None), "#test", "Test message")
        self.assertEquals(["Wallvoices"], n.callbacks)
    
    def testWallvoicesOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.wallvoices, (1, 7), "#test", "Test message")
        self.assertEquals([], n.callbacks)
    
    def testWallchops(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.wallchops((1, None), "#test", "Test message")
        self.assertEquals(["Wallchops"], n.callbacks)
    
    def testWallchopsOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(
            StateError, s.wallchops, (1, 7), "#test", "Test message")
        self.assertEquals([], n.callbacks)
    
    def testWallops(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.wallops((1, None), "Test message")
        self.assertEquals(["Wallops"], n.callbacks)
    
    def testWallopsOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.wallops, (1, 7), "Test message")
        self.assertEquals([], n.callbacks)
    
    def testWallusers(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.wallusers((1, None), "Test message")
        self.assertEquals(["Wallusers"], n.callbacks)
    
    def testWallusersOriginExists(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        self.assertRaises(StateError, s.wallusers, (1, 7), "Test message")
        self.assertEquals([], n.callbacks)
    
    def testDeregister_callbacks(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.wallusers((1, None), "Test message")
        self.assertEquals(["Wallusers"], n.callbacks)
        s.deregister_callback(State.CALLBACK_WALLUSERS, n.callback_wallusers)
        s.wallusers((1, None), "Test message")
        self.assertEquals(["Wallusers"], n.callbacks)
    
    def testDeregister_callbacksNoType(self):
        c = ConfigDouble()
        s = State(c)
        s.deregister_callback(State.CALLBACK_WALLUSERS,
                              self.testDeregister_callbacksNoType)
    
    def testDeregister_callbacksNotRegistered(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.deregister_callback(State.CALLBACK_WALLUSERS,
                              self.testDeregister_callbacksNotRegistered)
    
    def testGetNextHop(self):
        c = ConfigDouble()
        s = State(c)
        s.new_server((1, None), 2, "test.example.com", 1000, 1234, 1234, "P10",
            1, "", "A test example server")
        self.assertEquals(2, s.get_next_hop((2, None)))
        s.new_server((2, None), 3, "test2.example.com", 1000, 1234, 1234, "P10",
            1, "", "A test example server")
        self.assertEquals(2, s.get_next_hop((3, None)))
    
    def testOobmsg(self):
        c = ConfigDouble()
        s = State(c)
        n = self._setup_callbacks(s)
        s.oobmsg((1, None), (3,6), "123", ["Other arguments"])
        self.assertEquals(["Oobmsg"], n.callbacks)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
