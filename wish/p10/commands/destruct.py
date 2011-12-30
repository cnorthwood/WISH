#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class DestructHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.destroy_channel(origin, args[0], int(args[1]))
