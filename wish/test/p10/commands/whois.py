#!/usr/bin/env python

import unittest
from wish.p10.commands.whois import WhoIsHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = []
    
    def request_whois(self, origin, target, search):
        self.insight.append((target, search))

class WhoisTest(unittest.TestCase):
    
    def test_whois_single(self):
        s = StateDouble()
        c = WhoIsHandler(s)
        c.handle((1,1), ["AB", "Test"])
        self.assertEquals([((1, None), "Test")], s.insight)
    
    def test_whois_multi(self):
        s = StateDouble()
        c = WhoIsHandler(s)
        c.handle((1,1), ["AB", "Test,Second*"])
        self.assertEquals([((1, None), "Test"), ((1, None), "Second*")], s.insight)
