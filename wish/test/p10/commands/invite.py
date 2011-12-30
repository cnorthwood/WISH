#!/usr/bin/env python

import unittest

from wish.p10.commands.invite import InviteHandler

class StateDouble():
    
    def __init__(self):
        self.rv = None
    
    def nick2numeric(self, nick):
        return (1,8)
    
    def invite(self, origin, target, channel):
        self.rv = (target, channel)

class InviteTest(unittest.TestCase):
    
    def test_invite(self):
        s = StateDouble()
        c = InviteHandler(s)
        c.handle((1,1), ["test", "#foo"])
        self.assertEquals(((1,8), "#foo"), s.rv)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
