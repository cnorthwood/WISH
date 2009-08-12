#!/usr/bin/env python

import unittest
import p10.commands.squit

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def quitServer(self, origin, numeric, reason, ts):
        self.insight.append((origin, numeric, reason, ts))
    def nick2numeric(self, nick):
        return (2, None)
    
class SilenceTest(unittest.TestCase):
    
    def testAddSilence(self):
        s = StateDouble()
        c = p10.commands.squit.squit(s)
        c.handle((1,1), ["foo.example.com", "6", "A reason"])
        self.assertEquals([((1,1), (2, None), "A reason", 6)], s.insight)
