#!/usr/bin/env python

import genericcommand
import p10.base64

class nick(genericcommand.genericcommand):
    
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
            self._state.newUser(origin, (origin[0], p10.base64.toInt(args[-2])), args[0], args[3], args[4], modes, p10.base64.toInt(args[-3]), args[1], args[2], args[-1])
        else:
            self._state.changeNick(origin, origin, args[0], args[1])