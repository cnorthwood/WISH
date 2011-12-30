#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class CreateHandler(BaseCommand):
    """ Handles channel create commands """
    
    def handle(self, origin, args):
        for channel in args[0].split(','):
            # If we return false, we propogate this as a join and bounce a deop
            if not self._state.create_channel(origin, channel, args[1]):
                self._state.join_channel(origin, origin, channel, ["o"])
                self._state.deop((self._state.server_id, None), channel, origin)
