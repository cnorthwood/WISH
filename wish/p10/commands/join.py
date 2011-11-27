#!/usr/bin/env python

import genericcommand

class join(genericcommand.genericcommand):
    
    def handle(self, origin, args):
        channel = args[0]
        
        # Handle the "JOIN 0" case
        if channel == "0":
            self._state.partAllChannels(origin)
        # Normal joins
        else:
            if len(args) == 1:
                ts = 1270080000
            else:
                ts = int(args[1])
            self._state.joinChannel(origin, origin, channel, [], ts)