#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class WallChOpsHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.wallchops(origin, args[0], args[-1])
