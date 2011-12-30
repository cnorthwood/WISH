#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import to_int

class GlineHandler(BaseCommand):
    """
    Parses the GLINE changes
    """
    
    def handle(self, origin, line):
        if line[0] == "*":
            target = None
        else:
            target = to_int(line[0])
        # We don't care if it's forced or not
        if line[1][0] == "!":
            line[1] = line[1][1:]
        mask = line[1][1:]
        mode = line[1][0]
        if len(line) == 4:
            ts = self._state.ts
        else:
            ts = int(line[3])
        
        if mode == "+":
            duration = int(line[2])
            description = line[-1]
            self._state.add_gline(
                origin, mask, target, duration + self._state.ts, ts,
                description
            )
        else:
            self._state.remove_gline(origin, mask, target, ts)
