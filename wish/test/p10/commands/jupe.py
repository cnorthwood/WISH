#!/usr/bin/env python

import unittest
import time
from wish.p10.commands.jupe import JupeHandler

class StateDouble():
    
    def __init__(self):
        self.rv = None
    
    @property
    def ts(self):
        return 1
    
    def add_jupe(self, origin, server, target, expires, ts, reason):
        self.rv = ('add', server, expires)
    
    def remove_jupe(self, origin, server, target, ts):
        self.rv = ('del', server)
    
    @property
    def server_id(self):
        return 1


class JupeTest(unittest.TestCase):
    
    def test_add_jupe(self):
        s = StateDouble()
        c = JupeHandler(s)
        c.handle((1,None), ['*', '+test.example.com','26','43','Test jupe'])
        self.assertEquals(('add', 'test.example.com', 27), s.rv)
    
    def test_force_add_jupe(self):
        s = StateDouble()
        c = JupeHandler(s)
        c.handle((1,None), ['*', '!+test.example.com','26','43','Test jupe'])
        self.assertEquals(('add', 'test.example.com', 27), s.rv)
    
    def test_remove_jupe(self):
        s = StateDouble()
        c = JupeHandler(s)
        c.handle((1,None), ['*', '-test.example.com','26','43','Test jupe'])
        self.assertEquals(('del', 'test.example.com'), s.rv)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
