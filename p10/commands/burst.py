#!/usr/bin/env python

import genericcommand
import p10.base64

class burst(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        # Handle channel collisions
        cstatus = self._state.createChannel(origin, args[0], int(args[1]))
        nextarg = 2
        
        # Handle channel modes
        if len(args) > nextarg:
            if args[nextarg][0] == "+":
                # But only if this is a new channel
                if cstatus:
                    for mode in args[nextarg][1:]:
                        if mode == "k" or mode == "l":
                            nextarg = nextarg + 1
                            self._state.changeChannelMode(origin, args[0], (mode, args[nextarg]))
                        else:
                            self._state.changeChannelMode(origin, args[0], (mode, None))
                nextarg = nextarg + 1
        
        # Handle users on the channel
        if len(args) > nextarg:
            for user in args[nextarg].split(','):
                # Handle any user modes, but only if this is a new channel
                user = user.split(":")
                if len(user) > 1 and cstatus:
                    self._state.joinChannel(p10.base64.parseNumeric(user[0], self._state.maxClientNumerics), args[0],user[1])
                else:
                    self._state.joinChannel(p10.base64.parseNumeric(user[0], self._state.maxClientNumerics), args[0], "")
            nextarg = nextarg + 1
        
        # Handle channel bans, but only if this is a new channel
        if len(args) > nextarg and cstatus:
            if args[nextarg][0] == "%":
                for ban in args[nextarg][1:].split():
                    self._state.addChannelBan(origin, args[0], ban)