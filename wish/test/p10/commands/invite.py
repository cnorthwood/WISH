#!/usr/bin/env python

import unittest
import p10.commands.invite

class StateDouble:
    rv = None
    def __init__(self):
        self.rv = None
    def nick2numeric(self, nick):
        return (1,8)
    def invite(self, origin, target, channel):
        self.rv = (target, channel)

class InviteTest(unittest.TestCase):
    
    def testInvite(self):
        s = StateDouble()
        c = p10.commands.invite.invite(s)
        c.handle((1,1), ["test", "#foo"])
        self.assertEquals(((1,8), "#foo"), s.rv)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()