#!/usr/bin/env python

import p10.base64
import genericcommand

class mode(genericcommand.genericcommand):
    """ Changes user and channel modes """
    
    def handle(self, origin, args):
        finalmodes = []
        if args[0][0] == "#":
            # Channel mode changes
            channel = args[0]
            modes = args[1]
            nextarg = 2
            flag = "+"
            for mode in modes:
                if mode == "+" or mode == "-":
                    flag = mode
                # Limit only takes arg when set. Key always takes arg.
                elif mode == "k" or (mode == "l" and flag == "+"):
                    finalmodes.append((flag + mode, args[nextarg]))
                    nextarg = nextarg + 1
                elif mode == "b":
                    if flag == "-":
                        self._state.removeChannelBan(origin, channel, args[nextarg])
                        nextarg = nextarg + 1
                    else:
                        self._state.addChannelBan(origin, channel, args[nextarg])
                        nextarg = nextarg + 1
                elif mode == "o":
                    if flag == "-":
                        self._state.deop(origin, channel, p10.base64.parseNumeric(args[nextarg], self._state.maxClientNumerics))
                        nextarg = nextarg + 1
                    else:
                        self._state.op(origin, channel, p10.base64.parseNumeric(args[nextarg], self._state.maxClientNumerics))
                        nextarg = nextarg + 1
                elif mode == "v":
                    if flag == "-":
                        self._state.devoice(origin, channel, p10.base64.parseNumeric(args[nextarg], self._state.maxClientNumerics))
                        nextarg = nextarg + 1
                    else:
                        self._state.voice(origin, channel, p10.base64.parseNumeric(args[nextarg], self._state.maxClientNumerics))
                        nextarg = nextarg + 1
                else:
                    finalmodes.append((flag + mode, None))
            if len(finalmodes) > 0:
                self._state.changeChannelMode(origin, channel, finalmodes)
        else:
            # User mode changes
            modes = args[1]
            nextarg = 2
            flag = "+"
            finalmodes = []
            for mode in modes:
                if mode == "+" or mode == "-":
                    flag = mode
                #elif mode == "s":
                #    self._state.changeUserMode(origin, [(flag + mode, args[nextarg])])
                #    nextarg = nextarg + 1
                else:
                    finalmodes.append((flag + mode, None))
            self._state.changeUserMode(origin, finalmodes)