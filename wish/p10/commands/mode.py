#!/usr/bin/env python

from wish.p10.base64 import parse_numeric
from wish.p10.commands.basecommand import BaseCommand

class ModeHandler(BaseCommand):
    """
    Changes user and channel modes
    """
    
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
                        self._state.remove_channel_ban(
                            origin, channel, args[nextarg])
                        nextarg = nextarg + 1
                    else:
                        self._state.add_channel_ban(
                            origin, channel, args[nextarg])
                        nextarg = nextarg + 1
                elif mode == "o":
                    if flag == "-":
                        self._state.deop(
                            origin,
                            channel,
                            parse_numeric(args[nextarg],
                                          self._state.max_client_numerics)
                        )
                        nextarg = nextarg + 1
                    else:
                        self._state.op(
                            origin,
                            channel,
                            parse_numeric(args[nextarg],
                                          self._state.max_client_numerics)
                        )
                        nextarg = nextarg + 1
                elif mode == "v":
                    if flag == "-":
                        self._state.devoice(
                            origin,
                            channel,
                            parse_numeric(args[nextarg],
                                          self._state.max_client_numerics))
                        nextarg = nextarg + 1
                    else:
                        self._state.voice(
                            origin,
                            channel,
                            parse_numeric(args[nextarg],
                                          self._state.max_client_numerics))
                        nextarg = nextarg + 1
                else:
                    finalmodes.append((flag + mode, None))
            if len(finalmodes) > 0:
                self._state.change_channel_mode(origin, channel, finalmodes)
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
                #    self._state.change_user_mode(
                #        origin, [(flag + mode, args[nextarg])]
                #    )
                #    nextarg = nextarg + 1
                else:
                    finalmodes.append((flag + mode, None))
            self._state.change_user_mode(origin, finalmodes)
