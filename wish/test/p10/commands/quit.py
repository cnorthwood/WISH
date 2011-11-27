#!/usr/bin/env python

import unittest
import p10.commands.quit

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def quit(self, numeric, reason, causedbysquit=False):
        self.insight.append(reason)

class QuitTest(unittest.TestCase):
    
    def testQuit(self):
        s = StateDouble()
        c = p10.commands.quit.quit(s)
        c.handle((1,1), ["Reason"])
        self.assertEquals(["Reason"], s.insight)
