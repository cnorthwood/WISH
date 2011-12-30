#!/usr/bin/env python

import unittest
from wish.p10.commands.pong import PongHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = []
    
    def numeric2nick(self, num):
        if num == (1, None):
            return "test.example.com"
        else:
            return "test2.example.com"
    
    def register_pong(self, origin, source, target):
        self.insight.append((source, target))
    
    @property
    def server_id(self):
        return 1


class ServerDouble():
    
    numeric = 1
    
    def __init__(self):
        self.pung = False
    
    def register_pong(self):
        self.pung = True


class PongTest(unittest.TestCase):
    
    def test_local_pong(self):
        s = StateDouble()
        r = ServerDouble()
        c = PongHandler(s, r)
        c.handle((1,None), ["AD", "AB"])
        self.assertEquals([], s.insight)
        self.assertTrue(r.pung)
    
    def test_remote_pong(self):
        s = StateDouble()
        r = ServerDouble()
        c = PongHandler(s, r)
        c.handle((1,None), ["AD", "AC"])
        self.assertEquals([((3, None), (2, None))], s.insight)
        self.assertFalse(r.pung)
