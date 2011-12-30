#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class QuitHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.quit(origin, args[-1])
