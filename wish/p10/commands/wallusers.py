#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class WallUsersHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.wallusers(origin, args[-1])
