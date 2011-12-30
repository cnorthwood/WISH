#!/usr/bin/env python

import unittest
from wish.p10.commands.kill import KillHandler

class StateDouble():
    
    max_client_numerics = {1: 262143}
    
    def __init__(self):
        self.insight = None
    
    def kill(self, origin, target, path, reason):
        self.insight = (target, path, reason)


class KillTest(unittest.TestCase):
    
    def test_kill_only_one_remote(self):
        s = StateDouble()
        c = KillHandler(s)
        c.handle((1, 1), ["ABAAC", "test.example.com (Reason)"])
        self.assertEquals(((1,2), ["test.example.com"], "Reason"), s.insight)
    
    def test_kill_multi_remote(self):
        s = StateDouble()
        c = KillHandler(s)
        c.handle((1, 1), ["ABAAC", "test.example.com!origin.example.com (Reason)"])
        self.assertEquals(((1,2), ["test.example.com", "origin.example.com"], "Reason"), s.insight)
    
    def test_kill_multi_remote_multi_word_reason(self):
        s = StateDouble()
        c = KillHandler(s)
        c.handle((1, 1), ["ABAAC", "test.example.com!origin.example.com (Reason that is long)"])
        self.assertEquals(((1,2), ["test.example.com", "origin.example.com"], "Reason that is long"), s.insight)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
