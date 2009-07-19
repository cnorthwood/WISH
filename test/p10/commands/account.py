#!/usr/bin/env python

import unittest
import p10.commands.account

class StateDouble:
    numeric = None
    def authenticate(self, numeric, acname):
        self.numeric = numeric

class AccountTest(unittest.TestCase):
    
    def testSourceMustBeServer(self):
        s = StateDouble()
        c = p10.commands.account.account(s)
        self.assertRaises(p10.parser.ProtocolError, c.handle, (1, 1), ["ABAAB","Test"])
    
    def testPassToState(self):
        s = StateDouble()
        c = p10.commands.account.account(s)
        c.handle((1,None), ["ABAAB","Test"])
        self.assertEquals(s.numeric, (1,1))
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()