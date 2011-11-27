#!/usr/bin/env python

import unittest
import irc.motd

class StateDouble:
    insight = []
    users = dict()
    servers = dict()
    channels = dict()
    def __init__(self):
        self.insight = []
        self.maxClientNumerics = dict({1: 262143})
        self.users = dict({(1,1): irc.state.user((1,1), "test", "test", "example.com", [], 6, 0, 1234, "Joe Bloggs")})
        self.servers = dict({1: irc.state.server(None, 1, "test.example.com", 1234, 1234, 1234, "P10", 0, [], "A test description")})
        self.channels = dict({"#test": irc.state.channel("#test", 1234)})
    def getServerID(self):
        return 1
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    CALLBACK_REQUESTMOTD = "RequestMOTD"
    def registerCallback(self, type, callbackfn):
        pass
    def getServerID(self):
        return 1
    def getServerName(self):
        return "test.example.com"
    def numeric2nick(self, numeric):
        if numeric == (1, None):
            return "test.example.com"
        elif numeric == (2, None):
            return "test2.example.com"
        elif numeric == (3, None):
            return "test3.example.com"
        elif numeric == (1,6):
            return "localtest"
        elif numeric == (3, 2):
            return "test"

class IRCMOTDTest(unittest.TestCase):
    
    def testMOTDReply(self):
        s = StateDouble()
        c = irc.motd.motd(s)
        c.callbackMOTD(((3,6), (1, None)))
        self.assertEquals([((1,None), "375", (3,6), ["test.example.com Message of the Day"]), ((1,None), "376", (3,6), ["End of /MOTD."])], s.insight)
    
    def testMOTDReplyIfRelevant(self):
        s = StateDouble()
        c = irc.motd.motd(s)
        c.callbackMOTD(((7,6), (2, None)))
        self.assertEquals([], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()