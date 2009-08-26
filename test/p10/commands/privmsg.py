#!/usr/bin/env python

import unittest
import p10.commands.privmsg

class StateDouble:
    insight = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = []
    def privmsg(self, origin, target, message):
        self.insight.append((target, message))

class PrivmsgTest(unittest.TestCase):
    
    def testPrivmsg(self):
        s = StateDouble()
        c = p10.commands.privmsg.privmsg(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)
    
    def testPrivmsgUser(self):
        s = StateDouble()
        c = p10.commands.privmsg.privmsg(s)
        c.handle((1,1), ["ABAAB", "Test"])
        self.assertEquals([((1,1), "Test")], s.insight)
    
    def testPrivmsgSpecific(self):
        s = StateDouble()
        c = p10.commands.privmsg.privmsg(s)
        c.handle((1,1), ["foo@bar.com", "Test"])
        self.assertEquals([("foo@bar.com", "Test")], s.insight)
    
    def testPrivmsgServer(self):
        s = StateDouble()
        c = p10.commands.privmsg.privmsg(s)
        c.handle((1,1), ["$*.org", "Test"])
        self.assertEquals([("$*.org", "Test")], s.insight)