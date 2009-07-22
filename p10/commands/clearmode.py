#!/usr/bin/env python

import genericcommand

class clearmode(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        for mode in args[1]:
            if mode == "b":
                self._state.clearChannelBans(origin, args[0])
            elif mode == "o":
                self._state.clearChannelOps(origin, args[0])
            elif mode == "v":
                self._state.clearChannelVoices(origin, args[0])
            else:
                self._state.changeChannelMode(origin, args[0], ('-' + mode, None))