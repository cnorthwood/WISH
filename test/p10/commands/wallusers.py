#!/usr/bin/env python

import unittest
import p10.commands.wallusers

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def wallusers(self, origin, message):
        self.insight.append((message))

class WallusersTest(unittest.TestCase):
    
    def testWallusers(self):
        s = StateDouble()
        c = p10.commands.wallusers.wallusers(s)
        c.handle((1,1), ["Test"])
        self.assertEquals([("Test")], s.insight)