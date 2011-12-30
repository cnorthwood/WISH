#!/usr/bin/env python

import unittest
from wish.p10.commands.privmsg import PrivmsgHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = []
    
    def privmsg(self, origin, target, message):
        self.insight.append((target, message))


class PrivmsgTest(unittest.TestCase):
    
    def test_privmsg(self):
        s = StateDouble()
        c = PrivmsgHandler(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)
    
    def test_privmsg_user(self):
        s = StateDouble()
        c = PrivmsgHandler(s)
        c.handle((1,1), ["ABAAB", "Test"])
        self.assertEquals([((1,1), "Test")], s.insight)
    
    def test_privmsg_specific(self):
        s = StateDouble()
        c = PrivmsgHandler(s)
        c.handle((1,1), ["foo@bar.com", "Test"])
        self.assertEquals([("foo@bar.com", "Test")], s.insight)
    
    def test_privmsg_server(self):
        s = StateDouble()
        c = PrivmsgHandler(s)
        c.handle((1,1), ["$*.org", "Test"])
        self.assertEquals([("$*.org", "Test")], s.insight)
