#!/usr/bin/env python

import unittest
from wish.p10.commands.server import ServerHandler

class ConnectionDouble():
    
    def __init__(self):
        self.num = None
    def register_numeric(self, numeric):
        self.num = numeric


class StateDouble():
    
    def __init__(self):
        self.server = None
    
    def new_server(self, origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description):
        self.server = (origin, numeric, name, maxclient, boot_ts, link_ts, protocol, hops, flags, description)


class ServerTest(unittest.TestCase):
    
    def test_new_server(self):
        s = StateDouble()
        c = ServerHandler(s, None)
        c.handle((1,None), ["test.example.com", "2", "1234", "1234", "P10", "ADAAB", "+gh", "A new server introduced"])
        self.assertEquals(((1, None), 3, "test.example.com", 1, 1234, 1234, "P10", 2, [("+g", None), ("+h", None)], "A new server introduced"), s.server)
    
    def test_new_server_connection(self):
        s = StateDouble()
        conn = ConnectionDouble()
        c = ServerHandler(s, conn)
        c.handle((1,None), ["test.example.com", "2", "1234", "1234", "P10", "ADAAB", "+gh", "A new server introduced"])
        self.assertEquals(((1, None), 3, "test.example.com", 1, 1234, 1234, "P10", 2, [("+g", None), ("+h", None)], "A new server introduced"), s.server)
        self.assertEquals(3, conn.num)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
