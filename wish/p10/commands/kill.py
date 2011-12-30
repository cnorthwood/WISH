#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class KillHandler(BaseCommand):
    
    def handle(self, origin, args):
        target = args[0]
        info = args[1].split(None, 1)
        path = info[0].split("!")
        reason = info[1].strip("()")
        self._state.kill(
            origin,
            parse_numeric(target, self._state.max_client_numerics),
            path,
            reason
        )
