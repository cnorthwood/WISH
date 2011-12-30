#!/usr/bin/env python

import unittest
from wish.p10.commands.wallusers import WallUsersHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def wallusers(self, origin, message):
        self.insight.append((message))

class WallusersTest(unittest.TestCase):
    
    def test_wallusers(self):
        s = StateDouble()
        c = WallUsersHandler(s)
        c.handle((1,1), ["Test"])
        self.assertEquals([("Test")], s.insight)
