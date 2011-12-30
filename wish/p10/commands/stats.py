#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class StatsHandler(BaseCommand):
    
    def handle(self, origin, args):
        if len(args) > 2:
            extra = args[2]
        else:
            extra = None
        self._state.request_stats(
            origin,
            parse_numeric(args[1], self._state.max_client_numerics),
            args[0],
            extra
        )
