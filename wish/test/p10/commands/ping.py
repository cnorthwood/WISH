#!/usr/bin/env python

import unittest
from wish.p10.commands.ping import PingHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def numeric2nick(self, num):
        if num == (1, None):
            return "test.example.com"
        else:
            return "test2.example.com"
    
    def register_ping(self, origin, source, target):
        self.insight.append((source, target))
    
    @property
    def server_id(self):
        return 1


class ServerDouble():
    
    numeric = 2
    
    def __init__(self):
        self.pung = False
    
    def register_ping(self, source):
        self.pung = True


class PingTest(unittest.TestCase):
    
    def test_local_ping(self):
        s = StateDouble()
        r = ServerDouble()
        c = PingHandler(s, r)
        c.handle((1,None), ["AC"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)
    
    def test_remote_ping(self):
        s = StateDouble()
        r = ServerDouble()
        c = PingHandler(s, r)
        c.handle((1,None), ["AD", "test2.example.com"])
        self.assertEquals([("AD", "test2.example.com")], s.insight)
        self.assertFalse(r.pung)
    
    def test_remote_ping_local_dest(self):
        s = StateDouble()
        r = ServerDouble()
        c = PingHandler(s, r)
        c.handle((1,None), ["AD", "test.example.com"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)
