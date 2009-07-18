#!/usr/bin/env python

import unittest
import p10.state

class ConnectionDouble:
    numericID = 1
    called = False
    def send_line(self, source_client, token, args):
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

def main():
    unittest.main()

if __name__ == '__main__':
    main()