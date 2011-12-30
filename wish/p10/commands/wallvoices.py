#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class WallVoicesHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.wallvoices(origin, args[0], args[-1])
