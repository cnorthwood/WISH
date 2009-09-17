#!/usr/bin/env python

import unittest
import p10.commands.pong

class StateDouble:
    insight = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = []
    def numeric2nick(self, num):
        if num == (1, None):
            return "test.example.com"
        else:
            return "test2.example.com"
    def registerPong(self, origin, source, target):
        self.insight.append((source, target))
    def getServerID(self):
        return 1

class ServerDouble:
    pung = False
    numeric = 1
    def __init__(self):
        self.pung = False
    def registerPong(self):
        self.pung = True

class PongTest(unittest.TestCase):
    
    def testLocalPong(self):
        s = StateDouble()
        r = ServerDouble()
        c = p10.commands.pong.pong(s, r)
        c.handle((1,None), ["AD", "AB"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)
    
    def testRemotePong(self):
        s = StateDouble()
        r = ServerDouble()
        c = p10.commands.pong.pong(s, r)
        c.handle((1,None), ["AD", "AC"])
        self.assertEquals([((3, None), (2, None))], s.insight)
        self.assertFalse(r.pung)