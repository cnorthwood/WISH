#!/usr/bin/env python

import unittest
import p10.commands.admin

class StateDouble:
    numerics = []
    maxClientNumerics = dict({1: 262143})
    
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

class AdminTest(unittest.TestCase):
    
    def testSendsCorrectNumerics(self):
        s = StateDouble()
        a = p10.commands.admin.admin(s)
        a.handle((1,1), ["AB"])
        self.assertEquals(["256","257","258","259"], s.numerics)
        
    def testOnlySendIfWeAreDestination(self):
        s = StateDouble()
        a = p10.commands.admin.admin(s)
        a.handle((1,1), ["AF"])
        self.assertEquals([], s.numerics)

def main():
    unittest.main()

if __name__ == '__main__':
    main()