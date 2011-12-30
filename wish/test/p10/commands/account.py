#!/usr/bin/env python

import unittest

from wish.p10.commands.account import AccountHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def authenticate(self, origin, numeric, acname):
        self.numeric = numeric

class AccountTest(unittest.TestCase):
    
    def test_pass_to_state(self):
        s = StateDouble()
        c = AccountHandler(s)
        c.handle((1,None), ["ABAAB","Test"])
        self.assertEquals(s.numeric, (1,1))
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()
