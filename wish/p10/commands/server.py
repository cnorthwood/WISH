#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import to_int

class ServerHandler(BaseCommand):
    """
    Parses servers being introduced
    """
    
    def __init__(self, state, connection):
        self._connection = connection
        super(ServerHandler, self).__init__(state)
    
    def handle(self, origin, args):
        numeric = to_int(args[5][0:2])
        name = args[0]
        maxclients = to_int(args[5][2:5])
        boot_ts = int(args[2])
        link_ts = int(args[3])
        protocol = args[4]
        hops = int(args[1])
        modes = []
        flag = "+"
        for mode in args[6]:
            if mode == "+" or mode == "-":
                flag = mode
            else:
                modes.append((flag + mode, None))
        desc = args[-1]
        self._state.new_server(origin, numeric, name, maxclients, boot_ts,
                               link_ts, protocol, hops, modes, desc)
        if self._connection != None:
            self._connection.register_numeric(numeric)
