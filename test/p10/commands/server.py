#!/usr/bin/env python

import unittest
import p10.commands.server

class ConnectionDouble:
    num = None
    def __init__(self):
        self.num = None
    def registerNumeric(self, numeric):
        self.num = numeric

class StateDouble:
    server = None
    def __init__(self):
        self.server = None
    def newServer(self, origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description):
        self.server = (origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description)

class ServerTest(unittest.TestCase):
    
    def testNewServer(self):
        s = StateDouble()
        c = p10.commands.server.server(s, None)
        c.handle((1,None), ["test.example.com", "2", "1234", "1234", "P10", "ADAAB", "+gh", "A new server introduced"])
        self.assertEquals(((1, None), 3, "test.example.com", 1, 1234, 1234, "P10", 2, [("+g", None), ("+h", None)], "A new server introduced"), s.server)
    
    def testNewServerConnection(self):
        s = StateDouble()
        conn = ConnectionDouble()
        c = p10.commands.server.server(s, conn)
        c.handle((1,None), ["test.example.com", "2", "1234", "1234", "P10", "ADAAB", "+gh", "A new server introduced"])
        self.assertEquals(((1, None), 3, "test.example.com", 1, 1234, 1234, "P10", 2, [("+g", None), ("+h", None)], "A new server introduced"), s.server)
        self.assertEquals(3, conn.num)

def main():
    unittest.main()

if __name__ == '__main__':
    main()