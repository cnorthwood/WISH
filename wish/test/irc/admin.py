#!/usr/bin/env python

import unittest
import irc.admin

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def getServerID(self):
        return 1
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    CALLBACK_REQUESTADMIN = "RequestAdmin"
    def registerCallback(self, type, callbackfn):
        pass
    def getServerName(self):
        return "test.example.com"
    def getAdminName(self):
        return "tester"
    def getContactEmail(self):
        return "test@example.com"
    def getServerDescription(self):
        return "A testing server in Test, USA"

class IRCAdminTest(unittest.TestCase):
    
    def testAdminReply(self):
        s = StateDouble()
        c = irc.admin.admin(s)
        c.callbackAdminInfo(((3,6), (1, None)))
        self.assertEquals([((1,None), "256", (3,6), ["Administrative info about test.example.com"]), ((1,None), "257", (3,6), ["A testing server in Test, USA"]), ((1,None), "258", (3,6), ["Administrator is tester"]), ((1,None), "259", (3,6), ["test@example.com"])], s.insight)
    
    def testAdminReplyIfRelevant(self):
        s = StateDouble()
        c = irc.admin.admin(s)
        c.callbackAdminInfo(((7,6), (2, None)))
        self.assertEquals([], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()