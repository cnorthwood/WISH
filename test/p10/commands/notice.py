#!/usr/bin/env python

import unittest
import p10.commands.notice

class StateDouble:
    insight = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.insight = []
    def notice(self, origin, target, message):
        self.insight.append((target, message))

class NoticeTest(unittest.TestCase):
    
    def testNotice(self):
        s = StateDouble()
        c = p10.commands.notice.notice(s)
        c.handle((1,1), ["#test", "Test"])
        self.assertEquals([("#test", "Test")], s.insight)
    
    def testNoticeUser(self):
        s = StateDouble()
        c = p10.commands.notice.notice(s)
        c.handle((1,1), ["ABAAB", "Test"])
        self.assertEquals([((1,1), "Test")], s.insight)
    
    def testNoticeSpecific(self):
        s = StateDouble()
        c = p10.commands.notice.notice(s)
        c.handle((1,1), ["foo@bar.com", "Test"])
        self.assertEquals([("foo@bar.com", "Test")], s.insight)
    
    def testNoticeServer(self):
        s = StateDouble()
        c = p10.commands.notice.notice(s)
        c.handle((1,1), ["$*.org", "Test"])
        self.assertEquals([("$*.org", "Test")], s.insight)