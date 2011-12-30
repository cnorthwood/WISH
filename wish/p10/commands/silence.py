#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class SilenceHandler(BaseCommand):
    
    def handle(self, origin, args):
        if args[1][0] == "-":
            self._state.remove_silence(origin, args[1][1:])
        else:
            self._state.add_silence(origin, args[1])
