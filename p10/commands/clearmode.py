#!/usr/bin/env python

import genericcommand

class clearmode(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        for mode in args[1]:
            if mode == "b":
                self._state.clearChannelBans(args[0], False)
            elif mode == "o":
                self._state.clearChannelOps(args[0], False)
            elif mode == "v":
                self._state.clearChannelVoices(args[0], False)
            else:
                self._state.changeChannelMode(args[0], ('-' + mode, None), False)