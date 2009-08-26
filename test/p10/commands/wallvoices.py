#!/usr/bin/env python

import unittest
import p10.commands.wallvoices

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def wallvoices(self, origin, channel, message):
        self.insight.append((channel, message))

class WallvoiceTest(unittest.TestCase):
    
    def testWallvoice(self):
        s = StateDouble()
        c = p10.commands.wallvoices.wallvoices(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)