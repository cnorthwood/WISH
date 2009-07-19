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
        s.authenticate((1,1), "Test")
        self.assertEqual("Test", s.getAccountName((1,1)))
    
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

def main():
    unittest.main()

if __name__ == '__main__':
    main()