#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric, to_int

class NickHandler(BaseCommand):
    
    def handle(self, origin, args):
        # Parse mode string if exists, and any option arguments
        if origin[1] == None:
            modes = []
            if args[5][0] == "+":
                nextarg = 6
                for mode in args[5][1:]:
                    if mode == "r" or mode == "h":
                        modes.append(('+' + mode, args[nextarg]))
                        nextarg = nextarg + 1
                    else:
                        modes.append(('+' + mode, None))
            self._state.new_user(
                origin,
                parse_numeric(args[-2], self._state.max_client_numerics),
                args[0],
                args[3],
                args[4],
                modes,
                to_int(args[-3]),
                args[1],
                args[2],
                args[-1]
            )
        else:
            self._state.change_nick(origin, origin, args[0], args[1])
