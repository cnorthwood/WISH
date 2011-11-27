#!/usr/bin/env python

import unittest
import time
import p10.commands.jupe

class StateDouble:
    rv = None
    def __init__(self):
        self.rv = None
    def ts(self):
        return 1
    def addJupe(self, origin, server, target, expires, ts, reason):
        self.rv = ('add', server, expires)
    def removeJupe(self, origin, server, target, ts):
        self.rv = ('del', server)
    def getServerID(self):
        return 1

class JupeTest(unittest.TestCase):
    
    def testAddJupe(self):
        s = StateDouble()
        c = p10.commands.jupe.jupe(s)
        c.handle((1,None), ['*', '+test.example.com','26','43','Test jupe'])
        self.assertEquals(('add', 'test.example.com', 27), s.rv)
    
    def testForceAddJupe(self):
        s = StateDouble()
        c = p10.commands.jupe.jupe(s)
        c.handle((1,None), ['*', '!+test.example.com','26','43','Test jupe'])
        self.assertEquals(('add', 'test.example.com', 27), s.rv)
    
    def testRemoveJupe(self):
        s = StateDouble()
        c = p10.commands.jupe.jupe(s)
        c.handle((1,None), ['*', '-test.example.com','26','43','Test jupe'])
        self.assertEquals(('del', 'test.example.com'), s.rv)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()