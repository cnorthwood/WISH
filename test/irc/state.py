#!/usr/bin/env python

import unittest
import irc.state
import p10.parser

class ConfigDouble:
    numericID = 1
    serverName = "example.com"
    adminNick = "test"
    contactEmail = "test@example.com"
    called = False
    hiddenUserMask = ".users.example.com"

class ConnectionDouble:
    callbacks = []
    def __init__(self):
        self.callbacks = []
    def callbackNewUser(self, (origin, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname)):
        self.callbacks.append("NewUser")
    def callbackChangeNick(self, (origin, numeric, newnick, newts)):
        self.callbacks.append("ChangeNick")
    def callbackNewServer(self, (origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description)):
        self.callbacks.append("NewServer")
    def callbackAuthenticate(self, (origin, numeric, acname)):
        self.callbacks.append("Authenticate")
    def callbackAway(self, (numeric, reason)):
        self.callbacks.append("Away")
    def callbackBack(self, (numeric)):
        self.callbacks.append("Back")
    def callbackChannelCreate(self, (origin, name, ts)):
        self.callbacks.append("ChannelCreate")
    def callbackChannelJoin(self, (origin, numeric, name, modes, ts)):
        self.callbacks.append("ChannelJoin")
    def callbackChannelPart(self, (numeric, name, reason)):
        self.callbacks.append("ChannelPart")
    def callbackPartAll(self, (numeric)):
        self.callbacks.append("PartAll")
    def callbackChannelChangeMode(self, (origin, name, mode)):
        self.callbacks.append("ChannelChangeMode")
    def callbackChannelAddBan(self, (origin, name, mask)):
        self.callbacks.append("BanAdd")
    def callbackChannelRemoveBan(self, (origin, name, ban)):
        self.callbacks.append("BanRemove")
    def callbackChannelClearBans(self, (origin, name)):
        self.callbacks.append("ClearBans")
    def callbackChannelOp(self, (origin, channel, user)):
        self.callbacks.append("Op")
    def callbackChannelDeop(self, (origin, channel, user)):
        self.callbacks.append("Deop")
    def callbackChannelClearOps(self, (origin, name)):
        self.callbacks.append("ClearOps")
    def callbackChannelVoice(self, (origin, channel, user)):
        self.callbacks.append("Voice")
    def callbackChannelDevoice(self, (origin, channel, user)):
        self.callbacks.append("Devoice")
    def callbackChannelClearVoices(self, (origin, name)):
        self.callbacks.append("ClearVoices")
    def callbackGlineAdd(self, (origin, mask, target, expires, description)):
        self.callbacks.append("GlineAdd")
    def callbackGlineRemove(self, (origin, mask, target)):
        self.callbacks.append("GlineRemove")
    def callbackInvite(self, (origin, target, channel)):
        self.callbacks.append("Invite")
    def callbackJupeAdd(self, (origin, target, server, expire, reason)):
        self.callbacks.append("JupeAdd")
    def callbackJupeRemove(self, (origin, target, server)):
        self.callbacks.append("JupeRemove")
    def callbackAdminInfo(self, (origin, target)):
        self.callbacks.append("RequestAdmin")
    def callbackInfoRequest(self, (origin, target)):
        self.callbacks.append("RequestInfo")
    def callbackKick(self, (origin, channel, target, reason)):
        self.callbacks.append("ChannelKick")
    def callbackZombiePart(self, (origin, target)):
        self.callbacks.append("ChannelPartZombie")
    def callbackChannelDestroy(self, (origin, channel, ts)):
        self.callbacks.append("DestroyChannel")
    def callbackQuit(self, (numeric, reason)):
        self.callbacks.append(("Quit", reason))
    def callbackKill(self, (origin, target, path, reason)):
        self.callbacks.append(("Kill", path, reason))
    def callbackLusers(self, (origin, target, dummy)):
        self.callbacks.append("Lusers")
    def callbackLinks(self, (origin, target, mask)):
        self.callbacks.append("Links")
    def callbackChangeUserMode(self, (numeric, modes)):
        self.callbacks.append("ChangeUserMode")
    def callbackMOTD(self, (numeric, target)):
        self.callbacks.append("MOTD")
    def callbackNames(self, (origin, target, channel)):
        self.callbacks.append("Names")

class StateTest(unittest.TestCase):
    
    def _setupCallbacks(self, s):
        n = ConnectionDouble()
        s.registerCallback(irc.state.state.CALLBACK_NEWUSER, n.callbackNewUser)
        s.registerCallback(irc.state.state.CALLBACK_CHANGENICK, n.callbackChangeNick)
        s.registerCallback(irc.state.state.CALLBACK_NEWSERVER, n.callbackNewServer)
        s.registerCallback(irc.state.state.CALLBACK_AUTHENTICATE, n.callbackAuthenticate)
        s.registerCallback(irc.state.state.CALLBACK_USERMODECHANGE, n.callbackChangeUserMode)
        s.registerCallback(irc.state.state.CALLBACK_AWAY, n.callbackAway)
        s.registerCallback(irc.state.state.CALLBACK_BACK, n.callbackBack)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELCREATE, n.callbackChannelCreate)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELJOIN, n.callbackChannelJoin)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELPART, n.callbackChannelPart)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELPARTALL, n.callbackPartAll)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELMODECHANGE, n.callbackChannelChangeMode)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELBANADD, n.callbackChannelAddBan)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELBANREMOVE, n.callbackChannelRemoveBan)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELBANCLEAR, n.callbackChannelClearBans)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELOP, n.callbackChannelOp)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELDEOP, n.callbackChannelDeop)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELCLEAROPS, n.callbackChannelClearOps)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELVOICE, n.callbackChannelVoice)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELDEVOICE, n.callbackChannelDevoice)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELCLEARVOICES, n.callbackChannelClearVoices)
        s.registerCallback(irc.state.state.CALLBACK_GLINEADD, n.callbackGlineAdd)
        s.registerCallback(irc.state.state.CALLBACK_GLINEREMOVE, n.callbackGlineRemove)
        s.registerCallback(irc.state.state.CALLBACK_INVITE, n.callbackInvite)
        s.registerCallback(irc.state.state.CALLBACK_JUPEADD, n.callbackJupeAdd)
        s.registerCallback(irc.state.state.CALLBACK_JUPEREMOVE, n.callbackJupeRemove)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTADMIN, n.callbackAdminInfo)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTINFO, n.callbackInfoRequest)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELKICK, n.callbackKick)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELPARTZOMBIE, n.callbackZombiePart)
        s.registerCallback(irc.state.state.CALLBACK_CHANNELDESTROY, n.callbackChannelDestroy)
        s.registerCallback(irc.state.state.CALLBACK_QUIT, n.callbackQuit)
        s.registerCallback(irc.state.state.CALLBACK_KILL, n.callbackKill)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTLUSERS, n.callbackLusers)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTLINKS, n.callbackLinks)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTMOTD, n.callbackMOTD)
        s.registerCallback(irc.state.state.CALLBACK_REQUESTNAMES, n.callbackNames)
        return n
    
    def testAuthentication(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        s.authenticate((1, None), (1,1), "Test")
        self.assertEqual("Test", s.getAccountName((1,1)))
    
    def testCallbackAuthenticate(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.authenticate((1, None), (1,1), "Test")
        self.assertEquals(["Authenticate"], n.callbacks)
    
    def testAuthenticationOnlyExistingUsers(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.authenticate, (1, None), (1,1), "Test")
    
    def testAuthenticationOnlyOnce(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        s.authenticate((1, None), (1,1), "Test")
        self.assertRaises(irc.state.StateError, s.authenticate, (1, None), (1,1), "Test2")
    
    def testAuthenticationSourceMustBeServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        self.assertRaises(p10.parser.ProtocolError, s.authenticate, (1, 1), (1, 1), "Test")
        
    def testOnlyValidServerCanAuthUsers(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.authenticate, (8, None), (1, 1), "Test")
    
    def testGetNumericID(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertEqual(1, s.getServerID())
    
    def testGetServerName(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertEqual("example.com", s.getServerName())
    
    def testGetServerAdmin(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertEqual("test", s.getAdminName())
    
    def testGetServerEmail(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertEqual("test@example.com", s.getContactEmail())
    
    def testOnlyServerCanCreateUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(p10.parser.ProtocolError, s.newUser, (1, 6), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
    
    def testCorrectModesOnCreation(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.users[(1,1)].hasMode('o'))
        self.assertFalse(s.users[(1,1)].hasMode('b'))
    
    def testCorrectModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("+b","test"))
        self.assertEquals(s.users[(1,1)].hasMode('b'), "test")
    
    def testNegativeModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+b", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("-b",None))
        self.assertFalse(s.users[(1,1)].hasMode('b'))
    
    def testNewUserMustNotExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.newUser, (1, None), (1,1), "test2", "test2", "example.com", [("+r", "Test")], 6, 0, 0, "Duplicate Test User")
    
    def testNewUserAuthenticatesCorrectly(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+r", "test")], 0, 0, 0, "Test User")
        self.assertEquals("test", s.users[(1,1)].account)
    
    def testChangeNick(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.changeNick((1,1), (1,1), "test2", 2)
        self.assertEquals(s.users[(1,1)].nickname, "test2")
    
    def testChangeNickUnknownUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.changeNick, (1,None), (1,1), "test2", 2)
    
    def testMarkAway(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason")
        self.assertTrue(s.users[(1,1)].isAway())
    
    def testMarkAwayCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.setAway((1,1), "Away reason")
        self.assertEquals(["Away"], n.callbacks)
    
    def testMarkAwayNeedsParam(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.setAway, (1,1), "")
    
    def testMarkAwayNeedsExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.setAway, (1,1), "")
    
    def testMarkBack(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason")
        self.assertTrue(s.users[(1,1)].isAway())
        s.setBack((1,1))
        self.assertFalse(s.users[(1,1)].isAway())
    
    def testMarkBackCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.setBack((1,1))
        self.assertEquals(["Back"], n.callbacks)
    
    def testMarkBackNeedsExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.setBack, (1,1))
    
    def testCreateChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.createChannel((1,1), "#test", 6))
        self.assertTrue(s.channelExists("#test"))
        self.assertFalse(s.channelExists("#example"))
    
    def testCreateChannelCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.createChannel((1,1), "#test", 6)
        self.assertEquals(["ChannelCreate"], n.callbacks)
    
    def testCreateChannelClashBothOp(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,8), "test2", "test2", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.createChannel((1,1), "#test", 6))
        self.assertTrue(s.createChannel((1,8), "#test", 6))
        self.assertTrue(s.channelExists("#test"))
        self.assertTrue(s.channels["#test"].isop((1,1)))
        self.assertTrue(s.channels["#test"].isop((1,8)))
    
    def testCreateChannelEqualTSClashCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,8), "test2", "test2", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        n = self._setupCallbacks(s)
        s.createChannel((1,1), "#test", 6)
        s.createChannel((1,8), "#test", 6)
        self.assertEquals(["ChannelCreate", "ChannelJoin", "Op"], n.callbacks)
    
    def testCreateChannelUserJoinsIt(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.createChannel((1,1), "#test", 6))
        self.assertTrue(s.channelExists("#test"))
        self.assertTrue(s.channels["#test"].isop((1,1)))
    
    def testCreateChannelMustBeValidUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.createChannel, (1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.createChannel, (1,None), "#test", 6)
        self.assertFalse(s.channelExists("#test"))
    
    def testChannelJoinerMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.joinChannel, (1,8), (1,8), "#test", [])
    
    def testReplaceChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.createChannel((1,1), "#test", 6))
        self.assertTrue(s.channels["#test"].isop((1,1)))
        self.assertTrue(s.createChannel((1, 2), "#test", 3))
        self.assertEquals(3, s.channels["#test"].ts)
        self.assertFalse(s.channels["#test"].isop((1,1)))
        self.assertTrue(s.channels["#test"].isop((1,2)))
        self.assertFalse(s.createChannel((1, 1), "#test", 6))
    
    def testCreateChannelOverridesCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,8), "test2", "test2", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        n = self._setupCallbacks(s)
        s.createChannel((1,1), "#test", 6)
        s.createChannel((1,8), "#test", 3)
        self.assertEquals(["ChannelCreate", "ClearOps", "ClearVoices", "ClearBans", "ChannelJoin", "Op"], n.callbacks)
    
    def testSetChannelModes(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("p"))
        s.changeChannelMode((1,1), "#test", [("+p", None)])
        self.assertTrue(s.channels["#test"].hasMode("p"))
    
    def testSetChannelModesMulti(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("p"))
        self.assertFalse(s.channels["#test"].hasMode("k"))
        s.changeChannelMode((1,1), "#test", [("+p", None),("+k", "Test")])
        self.assertTrue(s.channels["#test"].hasMode("p"))
        self.assertEquals("Test", s.channels["#test"].hasMode("k"))
    
    def testSetChannelModesCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        n = self._setupCallbacks(s)
        s.changeChannelMode((1,1), "#test", [("+p", None)])
        self.assertEquals(["ChannelChangeMode"], n.callbacks)
    
    def testSetChannelModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("l"))
        s.changeChannelMode((1, 1), "#test", [("+l", "26")])
        self.assertEquals("26", s.channels["#test"].hasMode("l"))
    
    def testChannelModeChangerMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.changeChannelMode, (1,8), "#test", ("+l", "26"))
        self.assertRaises(irc.state.StateError, s.changeChannelMode, (4, None), "#test", ("+l", "26"))
    
    def testAddChannelBan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertTrue("*!*@*.example.com" in s.channels["#test"].bans)
    
    def testAddChannelBanCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        n = self._setupCallbacks(s)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["BanAdd"], n.callbacks)
    
    def testAddChannelBanNonExistantChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.addChannelBan, (1,None), "#test", "*!*@*.example.com")
    
    def testChannelBannerMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.addChannelBan, (1,8), "#test", "*!*@*.example.com")
        self.assertRaises(irc.state.StateError, s.addChannelBan, (4, None), "#test", "*!*@*.example.com")
        
    def testJoinNonExistentChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.joinChannel((1,1), (1,1), "#test", [])
        self.assertTrue(s.channelExists("#test"))
        self.assertTrue((1,1) in s.channels["#test"].users())
        self.assertTrue(s.channels["#test"].isop((1,1)))
    
    def testJoinCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,8), "test2", "test2", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        n = self._setupCallbacks(s)
        s.joinChannel((1,8), (1,8), "#test", [])
        self.assertEquals(["ChannelJoin"], n.callbacks)
    
    def testJoinButReallyCreateCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.joinChannel((1,1), (1,1), "#test", [])
        self.assertEquals(["ChannelCreate"], n.callbacks)
    
    def testChangeModeNonExistantChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.changeChannelMode, (1,1), "#test", ("+o", None))
    
    def testUnban(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.removeChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testUnbanCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        n = self._setupCallbacks(s)
        s.removeChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["BanRemove"], n.callbacks)
    
    def testUnbanMask(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.removeChannelBan((1, 1), "#test", "*!*@*.com")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testUnbanBadMask(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.removeChannelBan((1, 1), "#test", "*!*@notanexample.com")
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
    
    def testUnbanBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.removeChannelBan, (1, 1), "#test", ["*!*@*.example.com"])
    
    def testClearBans(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        s.clearChannelBans((1, 1), "#test")
        self.assertEquals([], s.channels["#test"].bans)
    
    def testClearBansCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.addChannelBan((1, 1), "#test", "*!*@*.example.com")
        n = self._setupCallbacks(s)
        s.clearChannelBans((1, 1), "#test")
        self.assertEquals(['ClearBans'], n.callbacks)
    
    def testClearBansBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.clearChannelBans,(1, 1), "#test")
    
    def testChannelBanRemoverMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.removeChannelBan, (1,8), "#test", "*!*@*.example.com")
        self.assertRaises(irc.state.StateError, s.removeChannelBan, (4, None), "#test", "*!*@*.example.com")
    
    def testChannelBanClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.clearChannelBans, (1,8), "#test")
        self.assertRaises(irc.state.StateError, s.clearChannelBans, (4, None), "#test")
    
    def testClearOps(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertEquals([(1,1)], s.channels["#test"].ops())
        s.clearChannelOps((1, 1), "#test")
        self.assertEquals([], s.channels["#test"].ops())
    
    def testClearOpsCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        n = self._setupCallbacks(s)
        s.clearChannelOps((1, 1), "#test")
        self.assertEquals(['ClearOps'], n.callbacks)
    
    def testChannelOpClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.clearChannelOps, (1,8), "#test")
        self.assertRaises(irc.state.StateError, s.clearChannelOps, (4, None), "#test")
    
    def testClearOpsBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.clearChannelOps, (1, 1), "#test")
    
    def testDeopBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.deop, (1,1), "#test", (1,1))
    
    def testOp(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        self.assertFalse(s.channels["#test"].isop((1,2)))
        s.op((1, 1), "#test", (1,2))
        self.assertTrue(s.channels["#test"].isop((1,2)))
    
    def testOpCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        n = self._setupCallbacks(s)
        s.op((1, 1), "#test", (1,2))
        self.assertEquals(['Op'], n.callbacks)
    
    def testOpBadUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.op, (1,1), "#test", (1,6))
    
    def testOpBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1,None),(1,6), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.op, (1,1), "#test", (1,6))
    
    def testDeopCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", ["o"])
        n = self._setupCallbacks(s)
        s.deop((1, 1), "#test", (1,2))
        self.assertEquals(['Deop'], n.callbacks)
    
    def testDeopBadUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.deop, (1,1), "#test", (1,6))
    
    def testClearVoices(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,1), (1,1), "#test", ["v"])
        self.assertEquals([(1,1)], s.channels["#test"].voices())
        s.clearChannelVoices((1,1), "#test")
        self.assertEquals([], s.channels["#test"].voices())
    
    def testClearVoicesCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", ["v"])
        n = self._setupCallbacks(s)
        s.clearChannelVoices((1, 1), "#test")
        self.assertEquals(['ClearVoices'], n.callbacks)
    
    def testChannelVoiceClearerMustExistOrServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.clearChannelVoices, (1,8), "#test")
        self.assertRaises(irc.state.StateError, s.clearChannelVoices, (4, None), "#test")
    
    def testClearVoicesBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.clearChannelVoices, (1,1), "#test")
    
    def testDevoiceBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.devoice, (1,1), "#test", (1,1))
    
    def testDevoiceBadUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.devoice, (1,1), "#test", (1,1))
    
    def testDevoiceCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", ["v"])
        n = self._setupCallbacks(s)
        s.devoice((1, 1), "#test", (1,2))
        self.assertEquals(['Devoice'], n.callbacks)
    
    def testVoice(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].isvoice((1,2)))
        s.joinChannel((1,2), (1,2), "#test", [])
        self.assertFalse(s.channels["#test"].isvoice((1,2)))
        s.voice((1, 1), "#test", (1,2))
        self.assertTrue(s.channels["#test"].isvoice((1,2)))
    
    def testVoiceCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        n = self._setupCallbacks(s)
        s.voice((1, 1), "#test", (1,2))
        self.assertEquals(['Voice'], n.callbacks)
    
    def testVoiceBadUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.voice, (1,1), "#test", (1,6))
    
    def testVoiceBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1,None),(1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1,None),(1,6), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.voice, (1,1), "#test", (1,6))
    
    def testNewServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        self.assertTrue(s.serverExists(2))
        self.assertEquals(1000, s.maxClientNumerics[2])
    
    def testNoDuplicateServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        self.assertRaises(irc.state.StateError, s.newServer, (1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
    
    def testOnlyServerCanIntroduceServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(p10.parser.ProtocolError, s.newServer, (1, 8), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
    
    def testOnlyExistingServerCanIntroduceServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.newServer, (177, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
    
    def testCurrentServerAlwaysExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertTrue(s.serverExists(1))
    
    def testOnlyValidServerCanCreateUsers(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.newUser, (8, None), (1,1), "test", "test", "example.com", [("+b", None)], 0, 0, 0, "Test User")
    
    def testAddGline(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
    
    def testAddGlineCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        self.assertEquals(["GlineAdd"], n.callbacks)
    
    def testIsGlinedMaskCheck(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("test!foo@bar.com"))
    
    def testGlinesExpire(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() - 3600, 6, "A test g-line")
        self.assertFalse(s.isGlined("test!foo@bar.com"))
    
    def testRemoveGline(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
        s.removeGline((1, 1), "*!foo@bar.com", None, 6)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
    
    def testRemoveGlineCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        n = self._setupCallbacks(s)
        s.removeGline((1, 1), "*!foo@bar.com", None, 6)
        self.assertEquals(["GlineRemove"], n.callbacks)
    
    def testRemoveGlineMask(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", None, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
        s.removeGline((1, 1), "*!*@bar.com", None, 6)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
    
    def testAddGlineSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", 1, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
    
    def testAddGlineNotSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", 8, s.ts() + 3600, 6, "A test g-line")
        self.assertFalse(s.isGlined("*!foo@bar.com"))
    
    def testRemoveGlineSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", 1, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
        s.removeGline((1, 1), "*!foo@bar.com", 1, 6)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
    
    def testRemoveGlineNotSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", 1, s.ts() + 3600, 6, "A test g-line")
        self.assertTrue(s.isGlined("*!foo@bar.com"))
        s.removeGline((1, 1), "*!foo@bar.com", 8, 6)
        self.assertTrue(s.isGlined("*!foo@bar.com"))
    
    def testGetGlobalGlines(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        expires = s.ts() + 3600
        s.addGline((1, 1), "*!foo@bar.com", 1, expires, 6, "A local test g-line")
        s.addGline((1, 1), "*!foo2@bar.com", None, expires, 6, "A global test g-line")
        s.addGline((1, 1), "*!foo3@bar.com", None, expires, 6, "A global deactivated g-line")
        s.removeGline((1,1), "*!foo3@bar.com", None, 6)
        self.assertEquals(2, len(s.glines()))
        self.assertTrue(("*!foo2@bar.com", "A global test g-line", expires, True, 6) in s.glines())
        self.assertTrue(("*!foo3@bar.com", "A global deactivated g-line", expires, False, 6) in s.glines())
    
    def testPartChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        self.assertTrue(s.channels["#test"].ison((1,1)))
        s.partChannel((1,1), "#test", "Test")
        self.assertFalse(s.channels["#test"].ison((1,1)))
    
    def testUnknownUserPartsChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.partChannel, (1,8), "#test", "Test")
    
    def testUserNotOnChannelPartsChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.partChannel, (1,2), "#test", "Test")
    
    def testPartingChannelMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.partChannel, (1,1), "#test", "Test")
    
    def testLastUserToPartsTurnsLightsOff(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        s.partChannel((1,1), "#test", "Test")
        s.partChannel((1,2), "#test", "Test")
        self.assertFalse(s.channelExists("#test"))
    
    def testUserPartsAllChannels(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        self.assertTrue(s.channels["#test"].ison((1,1)))
        s.partAllChannels((1,1))
        self.assertFalse(s.channels["#test"].ison((1,1)))
    
    def testInvite(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.invite((1,1), (1,2), "#test")
        self.assertTrue(s.users[(1,2)].isInvited("#test"))
    
    def testInviteCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        n = self._setupCallbacks(s)
        s.invite((1,1), (1,2), "#test")
        self.assertEquals(["Invite"], n.callbacks)
    
    def testInvitesAreHandedInOnJoin(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.invite((1,1), (1,2), "#test")
        s.joinChannel((1,2), (1,2), "#test", [])
        self.assertFalse(s.users[(1,2)].isInvited("#test"))
    
    def testChannelRemovalRemovesInvites(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        s.invite((1,1), (1,2), "#test")
        s.partChannel((1,1), "#test", "Test")
        self.assertFalse(s.users[(1,2)].isInvited("#test"))
    
    def testGetNumericFromNick(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        self.assertEquals((1,1), s.nick2numeric("test"))
        self.assertEquals((1,2), s.nick2numeric("test2"))
        self.assertEquals(None, s.nick2numeric("foo"))
    
    def testInviteTargetMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.invite, (1,1), (1,8), "#test")
    
    def testInviteChannelMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,8), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertRaises(irc.state.StateError, s.invite, (1,1), (1,8), "#test")
    
    def testCallbackNewUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertEquals(["NewUser"], n.callbacks)
    
    def testCallbacksCanBeMultiple(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n1 = self._setupCallbacks(s)
        n2 = self._setupCallbacks(s)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertEquals(["NewUser"], n1.callbacks)
        self.assertEquals(["NewUser"], n2.callbacks)
    
    def testCallbackChangeNick(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.changeNick((1,1), (1,1), "test2", 16000)
        self.assertEquals(["ChangeNick"], n.callbacks)
    
    def testCallbackNewServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        s.newServer((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        self.assertEquals(["NewServer"], n.callbacks)
    
    def testPartChannelCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        n = self._setupCallbacks(s)
        s.partChannel((1,1), "#test", "Test")
        self.assertEquals(["ChannelPart"], n.callbacks)
    
    def testPartAllChannelCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test2", "example.com", [("+l", None)], 0, 0, 0, "Test User 2")
        s.createChannel((1,1), "#test", 6)
        n = self._setupCallbacks(s)
        s.partAllChannels((1,1))
        self.assertEquals(["PartAll"], n.callbacks)
    
    def testAddJupe(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        self.assertTrue(s.isJuped("test.example.com"))
    
    def testAddJupeCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        self.assertEquals(["JupeAdd"], n.callbacks)
    
    def testJupesExpire(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() - 3600, 6, "Testing")
        self.assertFalse(s.isJuped("test.example.com"))
    
    def testAddJupeSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", 1, s.ts() + 3600, 6, "Testing")
        self.assertTrue(s.isJuped("test.example.com"))
    
    def testAddJupeSpecificTargetButNotUs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", 18, s.ts() + 3600, 6, "Testing")
        self.assertFalse(s.isJuped("test.example.com"))
    
    def testRemoveJupe(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        self.assertTrue(s.isJuped("test.example.com"))
        s.removeJupe((1,1), "test.example.com", None, 6)
        self.assertFalse(s.isJuped("test.example.com"))
    
    def testRemoveJupeCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        n = self._setupCallbacks(s)
        s.removeJupe((1,1), "test.example.com", None, 6)
        self.assertEquals(["JupeRemove"], n.callbacks)
    
    def testRemoveJupeSpecificTarget(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        s.removeJupe((1,1), "test.example.com", 1, 6)
        self.assertFalse(s.isJuped("test.example.com"))
    
    def testRemoveJupeSpecificTargetButNotUs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertFalse(s.isJuped("test.example.com"))
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.addJupe((1,1), "test.example.com", None, s.ts() + 3600, 6, "Testing")
        s.removeJupe((1,1), "test.example.com", 7, 6)
        self.assertTrue(s.isJuped("test.example.com"))
    
    def testGetGlobalJupes(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        expires = s.ts() + 3600
        s.addJupe((1,1), "test.example.com", 1, expires, 6, "Local jupe")
        s.addJupe((1, 1), "test2.example.com", None, expires, 6, "A global test jupe")
        s.addJupe((1, 1), "test3.example.com", None, expires, 6, "A global deactivated jupe")
        s.removeJupe((1,1), "test3.example.com", None, 6)
        self.assertEquals(2, len(s.jupes()))
        self.assertTrue(("test2.example.com", "A global test jupe", expires, True, 6) in s.jupes())
        self.assertTrue(("test3.example.com", "A global deactivated jupe", expires, False, 6) in s.jupes())
    
    def testSendAdminCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.sendAdminInfo((1,1), (1, None))
        self.assertEquals(["RequestAdmin"], n.callbacks)
    
    def testSendAdminCallbackOnlyIfOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendAdminInfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendAdminTargetMustBeServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendAdminInfo, (1,1), (1, 1))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendServerInfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoCallbackOnlyIfOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendServerInfo, (1,19), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendInfoTargetMustBeServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendServerInfo, (1,1), (1, 1))
        self.assertEquals([], n.callbacks)
    
    def testKickLocalUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        s.joinChannel((1,2), (1,2), "#test", [])
        n = self._setupCallbacks(s)
        s.kick((1,1), "#test", (1,2), "Testing")
        self.assertFalse(s.channels["#test"].ison((1,2)))
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickRemoteUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newServer((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newUser((6, None), (6,2), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        s.joinChannel((6,2), (6,2), "#test", [])
        n = self._setupCallbacks(s)
        s.kick((1,1), "#test", (6,2), "Testing")
        self.assertTrue(s.channels["#test"].ison((6,2)))
        self.assertFalse((6,2) in s.channels["#test"].users())
        self.assertEquals(["ChannelKick"], n.callbacks)
        s.partChannel((6,2), "#test", "bouncing kick")
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickOnInvalidChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(irc.state.StateError, s.kick, (1,1), "#test", (1,2), "Testing")
    
    def testKickOnInvalidUser(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertRaises(irc.state.StateError, s.kick, (1,1), "#test", (1,2), "Testing")
    
    def testKickingLastUserClosesChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        n = self._setupCallbacks(s)
        s.kick((1,1), "#test", (1,1), "Testing")
        self.assertFalse(s.channelExists("#test"))
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
    
    def testKickingLastUserRemoteDoesNotCloseChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newUser((6, None), (6,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        s.createChannel((6,2), "#test", 6)
        n = self._setupCallbacks(s)
        s.kick((6, None), "#test", (6,2), "Testing")
        self.assertTrue(s.channelExists("#test"))
        self.assertEquals(["ChannelKick"], n.callbacks)
        s.partChannel((6,2), "#test", "bouncing kick")
        self.assertEquals(["ChannelKick","ChannelPartZombie"], n.callbacks)
        self.assertFalse(s.channelExists("#test"))
    
    def testDestructChannelIgnoresFullChannels(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 6)
        self.assertTrue(s.channelExists("#test"))
        n = self._setupCallbacks(s)
        s.destroyChannel((1, None), "#test", 6)
        self.assertEquals([], n.callbacks)
        self.assertTrue(s.channelExists("#test"))
    
    def testDestructChannelIgnoresBadChannels(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.destroyChannel((1, None), "#test", 6)
        self.assertEquals(['DestroyChannel'], n.callbacks)
        self.assertFalse(s.channelExists("#test"))
    
    def testDestructChannelRemovesZombifiedChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newUser((6, None), (6,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        s.createChannel((6,2), "#test", 6)
        s.kick((6, None), "#test", (6,2), "Testing")
        self.assertTrue(s.channelExists("#test"))
        n = self._setupCallbacks(s)
        s.destroyChannel((6, None), "#test", 6)
        self.assertEquals(['DestroyChannel'], n.callbacks)
        self.assertFalse(s.channelExists("#test"))
    
    def testUserQuit(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.userExists((1,1)))
        s.quit((1,1), "A reason")
        self.assertFalse(s.userExists((1,1)))
    
    def testUserQuitCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.quit((1,1), "A reason")
        self.assertEquals([('Quit', 'A reason')], n.callbacks)
    
    def testUserQuitMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.quit, (1,1), "A reason")
    
    def testUserQuittingLeavesChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.newUser((1, None), (1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 16)
        s.joinChannel((1,2), (1,2), "#test", [])
        s.quit((1,2), "A reason")
        self.assertFalse(s.channels["#test"].ison((1,2)))
    
    def testLastUserQuittingClosesChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 16)
        s.quit((1,1), "A reason")
        self.assertFalse(s.channelExists("#test"))
    
    def testUserKillLocal(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 3, "origin.example.com", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.userExists((1,1)))
        n = self._setupCallbacks(s)
        s.kill((3,None), (1,1), [], "Testing")
        self.assertFalse(s.userExists((1,1)))
        self.assertEquals([("Quit", "Killed (Testing)")], n.callbacks)
    
    def testUserKillRemote(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 3, "origin.example.com", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newServer((1, None), 6, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        s.newUser((6, None), (6,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User 2")
        self.assertTrue(s.userExists((6,2)))
        n = self._setupCallbacks(s)
        s.kill((3,None), (6,2), [], "Testing")
        self.assertTrue(s.userExists((6,2)))
        self.assertEquals([("Kill", ["origin.example.com"], "Testing")], n.callbacks)
    
    def testSendLinksCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.sendLinksInfo((1,1), (1, None), "*.example.com")
        self.assertEquals(["Links"], n.callbacks)
    
    def testSendLinksCallbackOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendLinksInfo,(1,1), (1, None), "*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSendLinksCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendLinksInfo,(1,1), (1, 6), "*.example.com")
        self.assertEquals([], n.callbacks)
    
    def testSendLusersCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.sendLusersInfo((1,1), (1, None), "Dummy")
        self.assertEquals(["Lusers"], n.callbacks)
    
    def testSendLusersCallbackOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendLusersInfo,(1,1), (1, None), "dummy")
        self.assertEquals([], n.callbacks)
    
    def testSendLusersCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendLusersInfo,(1,1), (1, 6), "dummy")
        self.assertEquals([], n.callbacks)
    
    def testSendMOTDCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.sendMOTD((1,1), (1, None))
        self.assertEquals(["MOTD"], n.callbacks)
    
    def testSendMOTDCallbackOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendMOTD,(1,1), (1, None))
        self.assertEquals([], n.callbacks)
    
    def testSendMOTDCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendMOTD,(1,1), (1, 6))
        self.assertEquals([], n.callbacks)
    
    def testChangeUserMode(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.changeUserMode((1,1), [("+o", None)])
        self.assertTrue(s.users[(1,1)].hasMode("o"))
        self.assertEquals(['ChangeUserMode'], n.callbacks)
    
    def testChangeUserModeMultiple(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        s.changeUserMode((1,1), [("+o", None),("+h", "Test")])
        self.assertTrue(s.users[(1,1)].hasMode("o"))
        self.assertEquals("Test", s.users[(1,1)].hasMode("h"))
        self.assertEquals(['ChangeUserMode'], n.callbacks)
    
    def testChangeUserModeMustExist(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.changeUserMode, (1,1), [("+o", None),("+h", "Test")])
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallback(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 18)
        n = self._setupCallbacks(s)
        s.sendChannelUsers((1,1), (1, None), "#test")
        self.assertEquals(["Names"], n.callbacks)
    
    def testSendNamesCallbackOriginExists(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 18)
        n = self._setupCallbacks(s)
        self.assertRaises(irc.state.StateError, s.sendChannelUsers, (1,6), (1, None), "#test")
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallbackTargetIsServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1,1), "#test", 18)
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendChannelUsers, (1,1), (1, 6), "#test")
        self.assertEquals([], n.callbacks)
    
    def testSendNamesCallbackChannelisChannel(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        n = self._setupCallbacks(s)
        self.assertRaises(p10.parser.ProtocolError, s.sendChannelUsers, (1,1), (1, None), "#test")
        self.assertEquals([], n.callbacks)

def main():
    unittest.main()

if __name__ == '__main__':
    main()