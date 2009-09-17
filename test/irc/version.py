#!/usr/bin/env python

import unittest
import irc.version

class StateDouble:
    insight = []
    def __init__(self):
        self.insight = []
    def getServerID(self):
        return 1
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    CALLBACK_REQUESTVERSION = "RequestVersion"
    def registerCallback(self, type, callbackfn):
        pass

class IRCVersionTest(unittest.TestCase):
    
    def testVersionReply(self):
        s = StateDouble()
        c = irc.version.version(s)
        c.callbackRequestVersion(((3,6), (1, None)))
        self.assertEquals([((1,None), "351", (3,6), ["The WorldIRC Service Host - http://www.pling.org.uk/projects/wish/"])], s.insight)
    
    def testVersionReplyIfRelevant(self):
        s = StateDouble()
        c = irc.version.version(s)
        c.callbackRequestVersion(((7,6), (2, None)))
        self.assertEquals([], s.insight)

def main():
    unittest.main()

if __name__ == '__main__':
    main()