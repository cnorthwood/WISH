#!/usr/bin/env python

import genericcommand

class away(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        if len(args) > 0:
            if args[-1] == "":
                self._state.setBack(origin)
            else:
                self._state.setAway(origin, args[-1])
        else:
            self._state.setBack(origin)