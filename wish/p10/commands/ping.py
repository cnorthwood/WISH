#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class PingHandler(BaseCommand):
    
    def __init__(self, state, connection):
        self._connection = connection
        super(PingHandler, self).__init__(state)
    
    def handle(self, origin, args):
        if len(args) == 1:
            self._connection.register_ping(args[0])
        else:
            if args[1] == self._state.numeric2nick(
                (self._state.server_id, None)):
                self._connection.register_ping(args[0])
            else:
                self._state.register_ping(origin, args[0], args[1])
