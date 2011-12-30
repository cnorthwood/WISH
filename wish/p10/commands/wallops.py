#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class WallOpsHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.wallops(origin, args[-1])
