#!/usr/bin/env python

import unittest
import p10.commands.info

class StateDouble:
    numerics = []
    
    def __init__(self):
        self.numerics = []
    
    def sendLine(self, client, command, args):
        self.numerics.append(command)
    
    def getServerID(self):
        return 1
    
    def getServerName(self):
        return "example.com"
    
    def getNetworkName(self):
        return "example.com"
    
    def getAdminNick(self):
        return "test"
    
    def getContactEmail(self):
        return "text@example.com"

class InfoTest(unittest.TestCase):
    
    def testSendsCorrectNumerics(self):
        s = StateDouble()
        a = p10.commands.info.info(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(["371","374"], s.numerics)
        
    def testOnlySendIfWeAreDestination(self):
        s = StateDouble()
        a = p10.commands.info.info(s)
        a.handle((1,1), ["AF"])
        self.assertEquals([], s.numerics)

def main():
    unittest.main()

if __name__ == '__main__':
    main()