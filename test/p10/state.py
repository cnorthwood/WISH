#!/usr/bin/env python

import unittest
import p10.state
import time

class ConnectionDouble:
    numericID = 1
    serverName = "example.com"
    called = False
    line = []
    def __init__(self):
        self.called = False
        self.line = []
    def sendLine(self, source_client, token, args):
        self.called = True
        self.line.append(args)

class StateTest(unittest.TestCase):
    
    def testAuthentication(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User", False)
        s.authenticate((1,1), "Test", False)
        self.assertEqual("Test", s.getAccountName((1,1)))
        self.assertFalse(c.called)
    
    def testAuthenticationOnlyExistingUsers(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.authenticate, (1,1), "Test", False)
        self.assertFalse(c.called)
    
    def testAuthenticationOnlyOnce(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User", False)
        s.authenticate((1,1), "Test", False)
        self.assertRaises(p10.state.StateError, s.authenticate, (1,1), "Test2", False)
        self.assertFalse(c.called)
    
    def testLocalAuthSendsMessage(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User", False)
        s.authenticate((1,1), "Test", True)
        self.assertTrue(c.called)
        self.assertEqual([["ABAAB", "Test"]], c.line)
    
    def testSendMessage(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.sendLine(2, "TEST", ['foo'])
        self.assertTrue(c.called)
    
    def testGetNumericID(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertEqual(1, s.getServerID())
    
    def testGetServerName(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertEqual("example.com", s.getServerName())
    
    def testCorrectModesOnCreation(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertTrue(s.users[(1,1)].hasGlobalMode('o'))
        self.assertFalse(c.called)
    
    def testNewUserSendsLine(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", True)
        self.assertTrue(c.called)
        self.assertEquals([["test", "0", "0", "test", "example.com", "+o", "AAAAAA", "ABAAB", "Test User"]], c.line)
    
    def testCorrectModesWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.users[(1,1)].changeMode(("+b","test"))
        self.assertEquals(s.users[(1,1)].hasGlobalMode('b'), "test")
        self.assertFalse(c.called)
    
    def testNewUserSendsLineWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", "test")], 0, 0, 0, "Test User", True)
        self.assertTrue(c.called)
        self.assertEquals([["test", "0", "0", "test", "example.com", "+o", "test", "AAAAAA", "ABAAB", "Test User"]], c.line)
    
    def testNegativeModesWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+b", None)], 0, 0, 0, "Test User", False)
        s.users[(1,1)].changeMode(("-b",None))
        self.assertFalse(s.users[(1,1)].hasGlobalMode('b'))
        self.assertFalse(c.called)
    
    def testNewUserNoModesSendLine(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User", True)
        self.assertTrue(c.called)
        self.assertEquals([["test", "0", "0", "test", "example.com", "AAAAAA", "ABAAB", "Test User"]], c.line)
    
    def testNewUserMustNotExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertRaises(p10.state.StateError, s.newUser, (1,1), "test2", "test2", "example.com", [("+r", "Test")], 6, 0, 0, "Duplicate Test User", False)
        self.assertFalse(c.called)
    
    def testNewUserAuthenticatesCorrectly(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+r", "test")], 0, 0, 0, "Test User", False)
        self.assertEquals("test", s.users[(1,1)].account)
        self.assertFalse(c.called)
    
    def testChangeNick(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.changeNick((1,1), "test2", 2, False)
        self.assertEquals(s.users[(1,1)].nickname, "test2")
        self.assertFalse(c.called)
    
    def testChangeNickNewLine(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.changeNick((1,1), "test2", 2, True)
        self.assertEquals([["test2", "2"]], c.line)
        self.assertTrue(c.called)
    
    def testChangeNickUnknownUser(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.changeNick, (1,1), "test2", 2, False)
        self.assertFalse(c.called)
    
    def testMarkAway(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason", False)
        self.assertTrue(s.users[(1,1)].isAway())
    
    def testMarkAwaySendsLine(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.setAway((1,1), "Away reason", True)
        self.assertEquals([["Away reason"]], c.line)
        self.assertTrue(c.called)
    
    def testMarkAwayNeedsParam(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertRaises(p10.state.StateError, s.setAway, (1,1), "", True)
        self.assertFalse(c.called)
    
    def testMarkAwayNeedsExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.setAway, (1,1), "", True)
        self.assertFalse(c.called)
    
    def testMarkBack(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason", False)
        self.assertTrue(s.users[(1,1)].isAway())
        s.setBack((1,1), False)
        self.assertFalse(s.users[(1,1)].isAway())
    
    def testMarkBackSendsLine(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.setBack((1,1), True)
        self.assertEquals([[]], c.line)
        self.assertTrue(c.called)
    
    def testMarkBackNeedsExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.setBack, (1,1), False)
    
    def testCreateChannel(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertTrue(s.createChannel("#test", 6))
        self.assertTrue(s.channelExists("#test"))
        self.assertFalse(s.channelExists("#example"))
    
    def testReplaceChannel(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertTrue(s.createChannel("#test", 6))
        s.joinChannel("#test", (1,1), ["o"], False)
        self.assertTrue(s.channels["#test"].isop((1,1)))
        self.assertTrue(s.createChannel("#test", 3))
        self.assertEquals(3, s.channels["#test"].ts)
        self.assertFalse(s.channels["#test"].isop((1,1)))
        self.assertFalse(s.createChannel("#test", 6))
    
    def testSetChannelModes(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("p"))
        s.changeChannelMode("#test", ("+p", None), False)
        self.assertTrue(s.channels["#test"].hasMode("p"))
    
    def testSetChannelModesWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        self.assertFalse(s.channels["#test"].hasMode("l"))
        s.changeChannelMode("#test", ("+l", "26"), False)
        self.assertEquals("26", s.channels["#test"].hasMode("l"))
    
    def testAddChannelBan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        s.addChannelBan("#test", "*!*@*.example.com", False)
        self.assertTrue("*!*@*.example.com" in s.channels["#test"].bans)
    
    def testAddChannelBanNonExistantChannel(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.addChannelBan, "#test", "*!*@*.example.com", False)
    
    def testJoinNewChannelSendsCreate(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.joinChannel("#test", (1,1), [], True)
        self.assertEquals([["#test", str(int(time.time()))]], c.line)
        self.assertTrue(c.called)
    
    def testJoinNonExistentChannel(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.joinChannel("#test", (1,1), [], False)
        self.assertTrue(s.channelExists("#test"))
        self.assertTrue((1,1) in s.channels["#test"].users)
        self.assertTrue(s.channels["#test"].isop((1,1)))
    
    def testJoinSendsJoin(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.newUser((1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.newUser((1,3), "test3", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.createChannel("#test", 6)
        s.joinChannel("#test", (1,3), [], False)
        s.joinChannel("#test", (1,1), [], True)
        self.assertEquals([["#test", "6"]], c.line)
        self.assertTrue(c.called)
    
    def testJoinSendsOptionalModes(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.newUser((1,2), "test2", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.newUser((1,3), "test3", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.createChannel("#test", 6)
        s.joinChannel("#test", (1,3), [], False)
        s.joinChannel("#test", (1,1), ["o","v"], True)
        self.assertEquals([["#test", "6"],["#test", "+ov", "ABAAB", "ABAAB"]], c.line)
        self.assertTrue(c.called)
    
    def testJoinUserMustExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.joinChannel, "#test", (1,1), [], False)
    
    def testChangeModeNonExistantChannel(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.changeChannelMode, "#test", ("+o", None), False)
    
    def testChangeModeSendsLine(self):
        self.fail()
    
    def testBanSendsLine(self):
        self.fail()
    
    def testUnban(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        s.addChannelBan("#test", "*!*@*.example.com", False)
        self.assertEquals(["*!*@*.example.com"], s.channels["#test"].bans)
        s.removeChannelBan("#test", "*!*@*.example.com", False)
        self.assertEquals([], s.channels["#test"].bans)
    
    def testUnbanSendsLine(self):
        self.fail()
    
    def testUnbanBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.removeChannelBan, "#test", ["*!*@*.example.com"], False)
    
    def testClearBans(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        s.addChannelBan("#test", "*!*@*.example.com", False)
        s.clearChannelBans("#test", False)
        self.assertEquals([], s.channels["#test"].bans)
    
    def testClearBansSendsLine(self):
        self.fail()
    
    def testClearBansBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.clearChannelBans, "#test", False)
    
    def testClearOps(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.joinChannel("#test", (1,1), ["o"], False)
        self.assertEquals([(1,1)], s.channels["#test"].ops())
        s.clearChannelOps("#test", False)
        self.assertEquals([], s.channels["#test"].ops())
    
    def testClearOpsSendsLine(self):
        self.fail()
    
    def testClearOpsBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.clearChannelOps, "#test", False)
    
    def testDeopBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertRaises(p10.state.StateError, s.deop, "#test", (1,1), False)
    
    def testDeopBadUser(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        self.assertRaises(p10.state.StateError, s.deop, "#test", (1,1), False)
    
    def testDeopSendsLine(self):
        self.fail()
    
    def testClearVoices(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        s.joinChannel("#test", (1,1), ["v"], False)
        self.assertEquals([(1,1)], s.channels["#test"].voices())
        s.clearChannelVoices("#test", False)
        self.assertEquals([], s.channels["#test"].voices())
    
    def testClearVoiceSendsLine(self):
        self.fail()
    
    def testClearVoicesBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.clearChannelVoices, "#test", False)
    
    def testDevoiceBadChan(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User", False)
        self.assertRaises(p10.state.StateError, s.devoice, "#test", (1,1), False)
    
    def testDevoiceBadUser(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.createChannel("#test", 6)
        self.assertRaises(p10.state.StateError, s.devoice, "#test", (1,1), False)
    
    def testDevoiceSendsLine(self):
        self.fail()

def main():
    unittest.main()

if __name__ == '__main__':
    main()