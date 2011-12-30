#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class InviteHandler(BaseCommand):
    
    def handle(self, origin, args):
        target = self._state.nick2numeric(args[0])
        channel = args[1]
        self._state.invite(origin, target, channel)
