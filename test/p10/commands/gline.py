#!/usr/bin/env python

import unittest
import time
import p10.commands.gline

class StateDouble:
    rv = None
    def __init__(self):
        self.rv = None
    def ts(self):
        return 1
    def addGline(self, origin, mask, expires, description):
        self.rv = ('add', mask, expires)
    def removeGline(self, origin, mask):
        self.rv = ('del', mask)

class GlineTest(unittest.TestCase):
    
    def testAddGline(self):
        s = StateDouble()
        c = p10.commands.gline.gline(s)
        c.handle((1,None), ['*', '+test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 26+43), s.rv)
    
    def testForceAddGline(self):
        s = StateDouble()
        c = p10.commands.gline.gline(s)
        c.handle((1,None), ['*', '!+test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 26+43), s.rv)
    
    def testRemoveGline(self):
        s = StateDouble()
        c = p10.commands.gline.gline(s)
        c.handle((1,None), ['*', '-test!foo@example.com','26','43','Test gline'])
        self.assertEquals(('del', 'test!foo@example.com'), s.rv)
    
    def testAddGlineNoModTime(self):
        s = StateDouble()
        c = p10.commands.gline.gline(s)
        c.handle((1,None), ['*', '+test!foo@example.com','26','Test gline'])
        self.assertEquals(('add', 'test!foo@example.com', 27), s.rv)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()