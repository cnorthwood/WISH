#!/usr/bin/env python

import unittest
import time

from wish.p10.commands.gline import GlineHandler

class StateDouble():
    
    def __init__(self):
        self.rv = None
    
    @property
    def ts(self):
        return 1
    
    def add_gline(self, origin, mask, target, expires, ts, description):
        self.rv = ('add', mask, expires)
    
    def remove_gline(self, origin, mask, target, ts):
        self.rv = ('del', mask)
    
    @property
    def server_id(self):
        return 1

class GlineTest(unittest.TestCase):
    
    def test_add_gline(self):
        s = StateDouble()
        c = GlineHandler(s)
        c.handle((1,None), ['*', '+test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 27), s.rv)
    
    def test_force_add_gline(self):
        s = StateDouble()
        c = GlineHandler(s)
        c.handle((1,None), ['*', '!+test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 27), s.rv)
    
    def test_remove_gline(self):
        s = StateDouble()
        c = GlineHandler(s)
        c.handle((1,None), ['*', '-test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('del', 'test!foo@example.com'), s.rv)
    
    def test_add_gline_no_mod_time(self):
        s = StateDouble()
        c = GlineHandler(s)
        c.handle((1,None), ['*', '+test!foo@example.com','26','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 27), s.rv)
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
