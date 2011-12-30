#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class JoinHandler(BaseCommand):
    
    def handle(self, origin, args):
        channel = args[0]
        
        # Handle the "JOIN 0" case
        if channel == "0":
            self._state.part_all_channels(origin)
        # Normal joins
        else:
            if len(args) == 1:
                ts = 1270080000
            else:
                ts = int(args[1])
            self._state.join_channel(origin, origin, channel, [], ts)
