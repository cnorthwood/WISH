#!/usr/bin/env python

import unittest
from wish.p10.commands.squit import SQuitHandler

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    def quit_server(self, origin, numeric, reason, ts):
        self.insight.append((origin, numeric, reason, ts))
    
    def nick2numeric(self, nick):
        return (2, None)


class SQuitTest(unittest.TestCase):
    pass
