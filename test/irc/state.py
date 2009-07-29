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
    def sendLine(self, source_client, token, args):
        self.called = True

class StateTest(unittest.TestCase):
    
    def testAuthentication(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        s.authenticate((1, None), (1,1), "Test")
        self.assertEqual("Test", s.getAccountName((1,1)))
    
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
    
    def testSendMessage(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.sendLine(2, "TEST", ['foo'])
        self.assertTrue(c.called)
    
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
        self.assertTrue(s.users[(1,1)].hasGlobalMode('o'))
        self.assertFalse(s.users[(1,1)].hasGlobalMode('b'))
    
    def testCorrectModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("+b","test"))
        self.assertEquals(s.users[(1,1)].hasGlobalMode('b'), "test")
    
    def testNegativeModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+b", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("-b",None))
        self.assertFalse(s.users[(1,1)].hasGlobalMode('b'))
    
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
        self.assertRaises(irc.state.StateError, s.joinChannel, (1,8), "#test", [])
    
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
        self.assertFalse(s.createChannel((1, 1), "#test", 6))
    
    def testSetChannelModes(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("p"))
        s.changeChannelMode((1,1), "#test", ("+p", None))
        self.assertTrue(s.channels["#test"].hasMode("p"))
    
    def testSetChannelModesWithArgs(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newUser((1, None), (1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.createChannel((1, 1), "#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("l"))
        s.changeChannelMode((1, 1), "#test", ("+l", "26"))
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
        s.joinChannel((1,1), "#test", [])
        self.assertTrue(s.channelExists("#test"))
        self.assertTrue((1,1) in s.channels["#test"].users)
        self.assertTrue(s.channels["#test"].isop((1,1)))
    
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
    
    def testClearBansBadChan(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        self.assertRaises(irc.state.StateError, s.clearChannelBans,( 1, 1), "#test")
    
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
        s.joinChannel((1,1), "#test", ["v"])
        self.assertEquals([(1,1)], s.channels["#test"].voices())
        s.clearChannelVoices((1,1), "#test")
        self.assertEquals([], s.channels["#test"].voices())
    
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
    
    def testNewServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        self.assertTrue(s.serverExists(2))
    
    def testNoDuplicateServer(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.newServer((1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
        self.assertRaises(irc.state.StateError, s.newServer, (1, None), 2, "test.example.org", 1000, 0, 0, "P10", 1, "", "A testing server")
    
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
        self.assertEquals(None, s.isGlined("*!foo@bar.com"))
        s.addGline((1, 1), "*!foo@bar.com", s.ts() + 3600, "A test g-line")
        self.assertNotEquals(None, s.isGlined("*!foo@bar.com"))
    
    def testIsGlinedMaskCheck(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.addGline((1, 1), "*!foo@bar.com", s.ts() + 3600, "A test g-line")
        self.assertNotEquals(None, s.isGlined("test!foo@bar.com"))
    
    def testGlinesExpire(self):
        c = ConfigDouble()
        s = irc.state.state(c)
        s.addGline((1, 1), "*!foo@bar.com", s.ts() - 3600, "A test g-line")
        self.assertEquals(None, s.isGlined("test!foo@bar.com"))

def main():
    unittest.main()

if __name__ == '__main__':
    main()