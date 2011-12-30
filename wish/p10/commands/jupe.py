#!/usr/bin/env pytheon

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import to_int

class JupeHandler(BaseCommand):
    """ Parses the jupe changes """
    
    def handle(self, origin, line):
        if line[0] == "*":
            target = None
        else:
            target = to_int(line[0])
        # We don't care if it's forced or not
        if line[1][0] == "!":
            line[1] = line[1][1:]
        server = line[1][1:]
        mode = line[1][0]
        ts = int(line[3])
        
        if mode == "+":
            duration = int(line[2])
            description = line[-1]
            self._state.add_jupe(
                origin, server, target, duration + self._state.ts, ts,
                description
            )
        else:
            self._state.remove_jupe(origin, server, target, ts)
