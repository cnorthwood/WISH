#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class PartHandler(BaseCommand):
    
    def handle(self, origin, args):
        for channel in args[0].split(","):
            self._state.part_channel(origin, channel, args[-1])
