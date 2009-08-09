#!/usr/bin/env python

import genericcommand
import p10.base64

class server(genericcommand.genericcommand):
    """ Parses servers being introduced """
    
    def handle(self, origin, args):
        numeric = p10.base64.toInt(args[5][0:2])
        name = args[0]
        maxclients = p10.base64.toInt(args[5][2:5])
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
        self._state.newServer(origin, numeric, name, maxclients, boot_ts, link_ts, protocol, hops, modes, desc)