#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class SQuitHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.quit_server(
            origin, self._state.nick2numeric(args[0]), args[-1], int(args[1]))
