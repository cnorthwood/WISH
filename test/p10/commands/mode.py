#!/usr/bin/env python

import unittest
import time
import p10.commands.mode

class StateDouble:
    changes = []
    maxClientNumerics = dict({1: 262143})
    def __init__(self):
        self.changes = []
    def changeChannelMode(self, origin, name, modes):
        for mode in modes:
            self.changes.append(("ChannelModeChange", mode))
    def addChannelBan(self, origin, name, mask):
        self.changes.append(("Ban", name, mask))
    def removeChannelBan(self, origin, name, ban):
        self.changes.append(("Unban", name, ban))
    def op(self, origin, channel, user):
        self.changes.append(("Op", channel, user))
    def deop(self, origin, channel, user):
        self.changes.append(("Deop", channel, user))
    def voice(self, origin, channel, user):
        self.changes.append(("Voice", channel, user))
    def devoice(self, origin, channel, user):
        self.changes.append(("Devoice", channel, user))
    def changeUserMode(self, numeric, modes):
        for mode in modes:
            self.changes.append(("UserModeChange", mode))

class ModeTest(unittest.TestCase):
    
    # dioswkgxXInR
    def testUserModeChange(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['test', '+abc'])
        self.assertEquals([
            ('UserModeChange', ('+a', None)),
            ('UserModeChange', ('+b', None)),
            ('UserModeChange', ('+c', None))], s.changes)
    
    #def testUserModeChangeWithArg(self):
    #    s = StateDouble()
    #    c = p10.commands.mode.mode(s)
    #    c.handle((1,None), ['test', '+abs','1600'])
    #    self.assertEquals([
    #        ('UserModeChange', ('+a', None)),
    #        ('UserModeChange', ('+b', None)),
    #        ('UserModeChange', ('+s', '1600'))], s.changes)
    
    def testUserModeMix(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['test', '+ab-c'])
        self.assertEquals([
            ('UserModeChange', ('+a', None)),
            ('UserModeChange', ('+b', None)),
            ('UserModeChange', ('-c', None))], s.changes)
    
    # kl bov imnpstrDdcCNu
    def testChannelModeChange(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+ac', '26'])
        self.assertEquals([
            ('ChannelModeChange', ('+a', None)),
            ('ChannelModeChange', ('+c', None))], s.changes)
    
    def testChannelModeMix(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+a-c'])
        self.assertEquals([
            ('ChannelModeChange', ('+a', None)),
            ('ChannelModeChange', ('-c', None))], s.changes)
    
    def testChannelModeArgs(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+ak-c', 'test'])
        self.assertEquals([
            ('ChannelModeChange', ('+a', None)),
            ('ChannelModeChange', ('+k', 'test')),
            ('ChannelModeChange', ('-c', None))], s.changes)
    
    def testChannelModeArgsLimit(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+al-c', '26'])
        self.assertEquals([
            ('ChannelModeChange', ('+a', None)),
            ('ChannelModeChange', ('+l', '26')),
            ('ChannelModeChange', ('-c', None))], s.changes)
    
    def testUnsettingLimitNeedsNoArg(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+a-l+k', 'foo'])
        self.assertEquals([
            ('ChannelModeChange', ('+a', None)),
            ('ChannelModeChange', ('-l', None)),
            ('ChannelModeChange', ('+k', 'foo'))], s.changes)
    
    def testAddBan(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+b', '*!*foo@example.com'])
        self.assertEquals([('Ban', '#test', '*!*foo@example.com')], s.changes)
    
    def testUnban(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '-b', '*!*foo@example.com'])
        self.assertEquals([('Unban', '#test', '*!*foo@example.com')], s.changes)
    
    def testOp(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+o', 'ABAAB'])
        self.assertEquals([('Op', '#test', (1,1))], s.changes)
    
    def testDeop(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '-o', 'ABAAB'])
        self.assertEquals([('Deop', '#test', (1,1))], s.changes)
    
    def testVoice(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '+v', 'ABAAB'])
        self.assertEquals([('Voice', '#test', (1,1))], s.changes)
    
    def testDevoice(self):
        s = StateDouble()
        c = p10.commands.mode.mode(s)
        c.handle((1,None), ['#test', '-v', 'ABAAB'])
        self.assertEquals([('Devoice', '#test', (1,1))], s.changes)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()