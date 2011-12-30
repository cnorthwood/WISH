#!/usr/bin/env python

import unittest
from wish.p10.commands.nick import NickHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def change_nick(self, origin, numeric, newnick, newts):
        self.newnick = newnick
    
    def new_user(self, origin, numeric, nickname, username, hostname, modes, ip, hops, ts, fullname):
        self.newusernumeric = numeric
        self.newusernick = nickname
        self.newuserusername = username
        self.newuserhostname = hostname
        self.newusermodes = modes
        self.newuserip = ip
        self.newuserfullname = fullname


class NickTest(unittest.TestCase):
    
    def test_new_user_state_new_user_is_called(self):
        s = StateDouble()
        c = NickHandler(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+g', 'AAAAAB', 'ABAAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None)], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def test_new_user_no_modes(self):
        s = StateDouble()
        c = NickHandler(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', 'AAAAAB', 'ABAAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def test_new_user_mode_args(self):
        s = StateDouble()
        c = NickHandler(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+gh', 'test@example.com', 'AAAAAB', 'ABAAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None), ("+h", "test@example.com")], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def test_new_user_mode_args_multi(self):
        s = StateDouble()
        c = NickHandler(s)
        c.handle((1, None), ['Test', '1', '7', 'test', 'example.com', '+ghr', 'test@example.com', 'example', 'AAAAAB', 'ABAAC', 'Test User'])
        self.assertEquals((1,2), s.newusernumeric)
        self.assertEquals("Test", s.newusernick)
        self.assertEquals("test", s.newuserusername)
        self.assertEquals("example.com", s.newuserhostname)
        self.assertEquals([("+g", None), ("+h", "test@example.com"), ("+r", "example")], s.newusermodes)
        self.assertEquals(1, s.newuserip)
        self.assertEquals("Test User", s.newuserfullname)
    
    def test_nick_change(self):
        s = StateDouble()
        c = NickHandler(s)
        c.handle((1,1), ['test2', '666666'])
        self.assertEquals("test2", s.newnick)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()
