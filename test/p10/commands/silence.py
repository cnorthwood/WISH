#!/usr/bin/env python

import unittest
import p10.commands.silence

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def addSilence(self, numeric, mask):
        self.insight.append(('add', mask))
    def removeSilence(self, numeric, mask):
        self.insight.append(('remove', mask))

class SilenceTest(unittest.TestCase):
    
    def testAddSilence(self):
        s = StateDouble()
        c = p10.commands.silence.silence(s)
        c.handle((1,1), ["ABAAB", "foo!bar@example.com"])
        self.assertEquals([('add', 'foo!bar@example.com')], s.insight)
    
    def testDelSilence(self):
        s = StateDouble()
        c = p10.commands.silence.silence(s)
        c.handle((1,1), ["ABAAB", "-foo!bar@example.com"])
        self.assertEquals([('remove', 'foo!bar@example.com')], s.insight)
