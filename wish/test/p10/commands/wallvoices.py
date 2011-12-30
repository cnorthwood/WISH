#!/usr/bin/env python

import unittest
from wish.p10.commands.wallvoices import WallVoicesHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def wallvoices(self, origin, channel, message):
        self.insight.append((channel, message))

class WallvoiceTest(unittest.TestCase):
    
    def test_wallvoice(self):
        s = StateDouble()
        c = WallVoicesHandler(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)
