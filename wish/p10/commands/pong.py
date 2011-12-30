#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class PongHandler(BaseCommand):
    
    def __init__(self, state, connection):
        self._connection = connection
        BaseCommand.__init__(self, state)
    
    def handle(self, origin, args):
        if parse_numeric(args[1], self._state.max_client_numerics) \
           == \
           (self._state.server_id, None):
            self._connection.register_pong()
        else:
            self._state.register_pong(
                origin,
                parse_numeric(args[0], self._state.max_client_numerics),
                parse_numeric(args[1], self._state.max_client_numerics)
            )
