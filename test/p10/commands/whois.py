#!/usr/bin/env python

import unittest
import p10.commands.whois

class StateDouble:
    insight = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = []
    def requestWhois(self, origin, target, search):
        self.insight.append((target, search))

class WhoisTest(unittest.TestCase):
    
    def testWhoisSingle(self):
        s = StateDouble()
        c = p10.commands.whois.whois(s)
        c.handle((1,1), ["AB", "Test"])
        self.assertEquals([((1, None), "Test")], s.insight)
    
    def testWhoisMulti(self):
        s = StateDouble()
        c = p10.commands.whois.whois(s)
        c.handle((1,1), ["AB", "Test,Second*"])
        self.assertEquals([((1, None), "Test"), ((1, None), "Second*")], s.insight)