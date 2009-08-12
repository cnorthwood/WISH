#!/usr/bin/env python

import genericcommand

class silence(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        if args[1][0] == "-":
            self._state.removeSilence(origin, args[1][1:])
        else:
            self._state.addSilence(origin, args[1])