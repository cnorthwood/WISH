#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class BurstHandler(BaseCommand):
    
    def handle(self, origin, args):
        # Handle channel collisions
        cstatus = self._state.create_channel(origin, args[0], int(args[1]))
        nextarg = 2
        
        # Handle channel modes
        if len(args) > nextarg:
            if args[nextarg][0] == "+":
                # But only if this is a new channel
                if cstatus:
                    modes = []
                    for mode in args[nextarg][1:]:
                        if mode == "k" or mode == "l":
                            nextarg = nextarg + 1
                            modes.append(("+" + mode, args[nextarg]))
                        else:
                            modes.append(("+" + mode, None))
                    self._state.change_channel_mode(origin, args[0], modes)
                nextarg = nextarg + 1
        
        # Handle users on the channel
        if len(args) > nextarg:
            umodes = ""
            for user in args[nextarg].split(','):
                # Handle any user modes, but only if this is a new channel
                user = user.split(":")
                if len(user) > 1:
                    umodes = user[1]
                if cstatus:
                    self._state.join_channel(
                        parse_numeric(user[0], self._state.max_client_numerics),
                        parse_numeric(user[0], self._state.max_client_numerics),
                        args[0], umodes
                    )
                else:
                    self._state.join_channel(
                        parse_numeric(user[0], self._state.max_client_numerics),
                        parse_numeric(user[0], self._state.max_client_numerics),
                        args[0], ""
                    )
            nextarg = nextarg + 1
        
        # Handle channel bans, but only if this is a new channel
        if len(args) > nextarg and cstatus:
            if args[nextarg][0] == "%":
                for ban in args[nextarg][1:].split():
                    self._state.add_channel_ban(origin, args[0], ban)
