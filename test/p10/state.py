#!/usr/bin/env python

import unittest
import p10.state

class StateTest(unittest.TestCase):
    
    def testAuthentication(self):
        s = p10.state.state()
        s.authenticate((1,1), "Test")
        self.assertEqual("Test", s.getAccountName((1,1)))
    
    def testSendMessage(self):
        s = p10.state.state()

def main():
    unittest.main()

if __name__ == '__main__':
    main()