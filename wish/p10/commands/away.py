#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class AwayHandler(BaseCommand):
    
    def handle(self, origin, args):
        if len(args) > 0:
            if args[-1] == "":
                self._state.set_back(origin)
            else:
                self._state.set_away(origin, args[-1])
        else:
            self._state.set_back(origin)
