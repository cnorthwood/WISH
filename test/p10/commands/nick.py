#!/usr/bin/env python

import unittest
import p10.commands.nick

class StateDouble:
    newusernumeric = None
    newusernick = ""
    newuserusername = ""
    newuserhostname = ""
    newusermodes = []
    newuserip = 0
    newuserfullname = ""
    newnick = ""
    def changeNick(self, numeric, newnick):
        self.newnick = newnick
    def newUser(self, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname):
        self.newusernumeric = numeric
        self.newusernick = nickname
        self.newuserusername = username
        self.newuserhostname = hostname
        self.newusermodes = modes
        self.newuserip = ip
        self.newuserfullname = fullname

class NickTest(unittest.TestCase):
    
    def testNewUserStateNewUserIsCalled(self):
        s = StateDouble()
        c = p10.commands.nick.nick(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+g', 'AAAAAB', 'AAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None)], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def testNewUserNoModes(self):
        s = StateDouble()
        c = p10.commands.nick.nick(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', 'AAAAAB', 'AAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def testNewUserModeArgs(self):
        s = StateDouble()
        c = p10.commands.nick.nick(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+gh', 'test@example.com', 'AAAAAB', 'AAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None), ("+h", "test@example.com")], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def testNewUserModeArgsMulti(self):
        s = StateDouble()
        c = p10.commands.nick.nick(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+ghr', 'test@example.com', 'example', 'AAAAAB', 'AAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None), ("+h", "test@example.com"), ("+r", "example")], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def testNickChange(self):
        s = StateDouble()
        c = p10.commands.nick.nick(s)
        c.handle((1,1), ['test2', '666666'])
        self.assertEquals("test2", s.newnick)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()