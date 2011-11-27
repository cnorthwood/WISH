#!/usr/bin/env python

import unittest
import p10.commands.numberrelay

class StateDouble:
    insight = None
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = None
    def oobmsg(self, origin, type, args):
        self.insight = (origin, type, args)

class NumberRelayTest(unittest.TestCase):
    
    def testPassToState(self):
        s = StateDouble()
        c = p10.commands.numberrelay.numberrelay(s, "123")
        c.handle((1,None), ["ABAAB", "Test"])
        self.assertEquals(((1, None), "123", ["ABAAB", "Test"]), s.insight)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()