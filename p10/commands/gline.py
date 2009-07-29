#!/usr/bin/env python

import genericcommand

class gline(genericcommand.genericcommand):
    """ Parses the GLINE changes """
    
    def handle(self, origin, line):
        # We don't care if it's forced or not
        if line[1][0] == "!":
            line[1] = line[1][1:]
        mask = line[1][1:]
        mode = line[1][0]
        
        if mode == "+":
            duration = int(line[2])
            if len(line) == 4:
                ts = self._state.ts()
            else:
                ts = int(line[3])
            description = line[-1]
            self._state.addGline(origin, mask, duration + ts, description)
        else:
            self._state.removeGline(origin, mask)