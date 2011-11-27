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
    
class SquitTest(unittest.TestCase):
    pass
