#!/usr/bin/env pytheon

import genericcommand
import p10.base64

class jupe(genericcommand.genericcommand):
    """ Parses the GLINE changes """
    
    def handle(self, origin, line):
        if line[0] == "*":
            target = None
        else:
            target = p10.base64.toInt(line[0])
        # We don't care if it's forced or not
        if line[1][0] == "!":
            line[1] = line[1][1:]
        server = line[1][1:]
        mode = line[1][0]
        ts = int(line[3])
        
        if mode == "+":
            duration = int(line[2])
            description = line[-1]
            self._state.addJupe(origin, server, target, duration + self._state.ts(), ts, description)
        else:
            self._state.removeJupe(origin, server, target, ts)