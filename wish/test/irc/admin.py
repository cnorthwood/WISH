#!/usr/bin/env python

import unittest

from wish.irc.admin import AdminResponder

class StateDouble():
    
    def __init__(self):
        self.insight = []
    
    @property
    def server_id(self):
        return 1
    
    def oobmsg(self, origin, target, type, args):
        self.insight.append((origin, type, target, args))
    
    CALLBACK_REQUESTADMIN = "RequestAdmin"
    
    def register_callback(self, type, callbackfn):
        pass
    
    @property
    def server_name(self):
        return "test.example.com"
    
    @property
    def admin_name(self):
        return "tester"
    
    @property
    def contact_email(self):
        return "test@example.com"
    
    @property
    def server_description(self):
        return "A testing server in Test, USA"


class IRCAdminTest(unittest.TestCase):
    
    def test_admin_reply(self):
        s = StateDouble()
        c = AdminResponder(s)
        c.callback_admininfo((3,6), (1, None))
        self.assertEquals(
            [
                (
                    (1,None),
                    "256",
                    (3,6),
                    ["Administrative info about test.example.com"]
                ), (
                    (1,None),
                    "257",
                    (3,6),
                    ["A testing server in Test, USA"]
                ), (
                    (1,None),
                    "258",
                    (3,6),
                    ["Administrator is tester"]
                ), (
                    (1,None),
                    "259",
                    (3,6),
                    ["test@example.com"]
                )
            ],
            s.insight
        )
    
    def test_admin_reply_if_relevant(self):
        s = StateDouble()
        c = AdminResponder(s)
        c.callback_admininfo((7,6), (2, None))
        self.assertEquals([], s.insight)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
