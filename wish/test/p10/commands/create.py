#!/usr/bin/env python

import unittest
import p10.commands.create
import threading

class StateDouble:
    rv = True
    created = list()
    joincalled = False
    deopcalled = False
    lock = None
    def __init__(self):
        self.rv = True
        self.created = list()
        self.joincalled = False
        self.deopcalled = False
        self.lock = threading.RLock()
    def createChannel(self, origin, name, ts):
        self.created.append(name)
        return self.rv
    def joinChannel(self, origin, numeric, name, modes):
        self.joincalled = True
    def deop(self, origin, channel, user):
        self.deopcalled = True
    def getServerID(self):
        return 1

class CreateTest(unittest.TestCase):
    
    def testCreateCalled(self):
        s = StateDouble()
        c = p10.commands.create.create(s)
        c.handle((1,1), ['#foo', '1234567'])
        self.assertEquals(['#foo'], s.created)
    
    def testCreateMultiArgs(self):
        s = StateDouble()
        c = p10.commands.create.create(s)
        c.handle((1,1), ['#foo,#bar', '1234567'])
        self.assertEquals(['#foo', '#bar'], s.created)
    
    def testCreateClashAndBounce(self):
        s = StateDouble()
        c = p10.commands.create.create(s)
        s.rv = False
        c.handle((1,1),  ['#foo', '1234567'])
        self.assertTrue(s.joincalled)
        self.assertTrue(s.deopcalled)
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()