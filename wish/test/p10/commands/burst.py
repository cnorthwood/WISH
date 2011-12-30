#!/usr/bin/env python

import unittest

from wish.p10.commands.burst import BurstHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.rv = True
        self.modes = []
        self.users = []
        self.ts = 0
        self.bans = []
    
    def create_channel(self, origin, name, ts):
        self.ts = ts
        return self.rv
    
    def change_channel_mode(self, origin, name, modes):
        for mode in modes:
            self.modes.append(mode)
    
    def join_channel(self, origin, numeric, name, modes):
        self.users.append((numeric, modes))
    
    def add_channel_ban(self, origin, name, mask):
        self.bans.append(mask)


class BurstTest(unittest.TestCase):
    
    def testNormalCreate(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB"])
        self.assertEquals([('+c', None)], s.modes)
        self.assertEquals([((1,1), "")], s.users)
        self.assertEquals(8, s.ts)
    
    def testMultiUserCreate(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB,ABAAD"])
        self.assertEquals([((1,1), ""), ((1,3), "")], s.users)
    
    def testMultiUserWithModesCreate(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB,ABAAD:o"])
        self.assertEquals([((1,1), ""), ((1,3), "o")], s.users)
    
    def testMultiUserWithMultiModesCreate(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB,ABAAD:o,ABAAE"])
        self.assertEquals([((1,1), ""), ((1,3), "o"), ((1,4), "o")], s.users)
    
    def testNoModeOnlyUsers(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "ABAAB,ABAAD"])
        self.assertEquals([], s.modes)
        self.assertEquals([((1,1), ""), ((1,3), "")], s.users)
    
    def testModeArgsCreate(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+l", "42", "ABAAB,ABAAD"])
        self.assertEquals([("+l","42")], s.modes)
    
    def testCreateWithBans(self):
        s = StateDouble()
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB", "%*!*@*.example.com"])
        self.assertEquals(['*!*@*.example.com'], s.bans)
    
    def testChannelCollisions(self):
        s = StateDouble()
        s.rv = False
        s.modes = [('+a', None)]
        s.users = [((1,2), ""), ((1,8), "")]
        c = BurstHandler(s)
        c.handle((1,None), ["#test", "8", "+c", "ABAAB:ov", "%*!*@*.example.com"])
        self.assertEquals([('+a', None)], s.modes)
        self.assertEquals([((1,2), ""), ((1,8), ""), ((1,1), "")], s.users)
        self.assertEquals([], s.bans)
        
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()
