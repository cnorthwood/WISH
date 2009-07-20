#!/usr/bin/env python

import unittest
import p10.state

class ConnectionDouble:
    numericID = 1
    serverName = "example.com"
    called = False
    def sendLine(self, source_client, token, args):
        self.called = True

class StateTest(unittest.TestCase):
    
    def testAuthentication(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        s.authenticate((1,1), "Test")
        self.assertEqual("Test", s.getAccountName((1,1)))
    
    def testAuthenticationOnlyExistingUsers(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.authenticate, (1,1), "Test")
    
    def testAuthenticationOnlyOnce(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [], 0, 0, 0, "Test User")
        s.authenticate((1,1), "Test")
        self.assertRaises(p10.state.StateError, s.authenticate, (1,1), "Test2")
    
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
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertTrue(s.users[(1,1)].hasGlobalMode('o'))
    
    def testCorrectModesWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("+b","test"))
        self.assertEquals(s.users[(1,1)].hasGlobalMode('b'), "test")
    
    def testNegativeModesWithArgs(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+b", None)], 0, 0, 0, "Test User")
        s.users[(1,1)].changeMode(("-b",None))
        self.assertFalse(s.users[(1,1)].hasGlobalMode('b'))
    
    def testNewUserMustNotExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(p10.state.StateError, s.newUser, (1,1), "test2", "test2", "example.com", [("+r", "Test")], 6, 0, 0, "Duplicate Test User")
    
    def testNewUserAuthenticatesCorrectly(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+r", "test")], 0, 0, 0, "Test User")
        self.assertEquals("test", s.users[(1,1)].account)
    
    def testChangeNick(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        s.changeNick((1,1), "test2", 2)
        self.assertEquals(s.users[(1,1)].nickname, "test2")
    
    def testChangeNickUnknownUser(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.changeNick, (1,1), "test2", 2)
    
    def testMarkAway(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason")
        self.assertTrue(s.users[(1,1)].isAway())
    
    def testMarkAwayNeedsParam(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertRaises(p10.state.StateError, s.setAway, (1,1), "")
    
    def testMarkAwayNeedsExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.setAway, (1,1), "")
    
    def testMarkBack(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        s.newUser((1,1), "test", "test", "example.com", [("+o", None)], 0, 0, 0, "Test User")
        self.assertFalse(s.users[(1,1)].isAway())
        s.setAway((1,1), "Away reason")
        self.assertTrue(s.users[(1,1)].isAway())
        s.setBack((1,1))
        self.assertFalse(s.users[(1,1)].isAway())
    
    def testMarkBackNeedsExist(self):
        c = ConnectionDouble()
        s = p10.state.state(c)
        self.assertRaises(p10.state.StateError, s.setBack, (1,1))

def main():
    unittest.main()

if __name__ == '__main__':
    main()