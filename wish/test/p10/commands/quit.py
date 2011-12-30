#!/usr/bin/env python

import unittest
from wish.p10.commands.quit import QuitHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def quit(self, numeric, reason, causedbysquit=False):
        self.insight.append(reason)


class QuitTest(unittest.TestCase):
    
    def test_quit(self):
        s = StateDouble()
        c = QuitHandler(s)
        c.handle((1,1), ["Reason"])
        self.assertEquals(["Reason"], s.insight)
