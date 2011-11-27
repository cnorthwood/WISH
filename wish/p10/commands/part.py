#!/usr/bin/env python

import genericcommand

class part(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        for channel in args[0].split(","):
            self._state.partChannel(origin, channel, args[-1])