#!/usr/bin/env python

import unittest
import p10.commands.kill

class StateDouble:
    insight = None
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = None
    def kill(self, origin, target, path, reason):
        self.insight = (target, path, reason)

class KillTest(unittest.TestCase):
    
    def testKillOnlyOneRemote(self):
        s = StateDouble()
        c = p10.commands.kill.kill(s)
        c.handle((1, 1), ["ABAAC", "test.example.com (Reason)"])
        self.assertEquals(((1,2), ["test.example.com"], "Reason"), s.insight)
    
    def testKillMultiRemote(self):
        s = StateDouble()
        c = p10.commands.kill.kill(s)
        c.handle((1, 1), ["ABAAC", "test.example.com!origin.example.com (Reason)"])
        self.assertEquals(((1,2), ["test.example.com", "origin.example.com"], "Reason"), s.insight)
    
    def testKillMultiRemoteMultiWordReason(self):
        s = StateDouble()
        c = p10.commands.kill.kill(s)
        c.handle((1, 1), ["ABAAC", "test.example.com!origin.example.com (Reason that is long)"])
        self.assertEquals(((1,2), ["test.example.com", "origin.example.com"], "Reason that is long"), s.insight)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()