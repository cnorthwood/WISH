#!/usr/bin/env python

import unittest
import p10.commands.ping

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def numeric2nick(self, num):
        if num == (1, None):
            return "test.example.com"
        else:
            return "test2.example.com"
    def registerPing(self, origin, source, target):
        self.insight.append((source, target))

class ServerDouble:
    pung = False
    numeric = 1
    def __init__(self):
        self.pung = False
    def registerPing(self, source):
        self.pung = True

class PingTest(unittest.TestCase):
    
    def testLocalPing(self):
        s = StateDouble()
        r = ServerDouble()
        c = p10.commands.ping.ping(s, r)
        c.handle((1,None), ["AC"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)
    
    def testRemotePing(self):
        s = StateDouble()
        r = ServerDouble()
        c = p10.commands.ping.ping(s, r)
        c.handle((1,None), ["AD", "test2.example.com"])
        self.assertEquals([("AD", "test2.example.com")], s.insight)
        self.assertFalse(r.pung)
    
    def testRemotePingLocalDest(self):
        s = StateDouble()
        r = ServerDouble()
        c = p10.commands.ping.ping(s, r)
        c.handle((1,None), ["AD", "test.example.com"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)