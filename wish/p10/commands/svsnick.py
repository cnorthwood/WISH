#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class SvsNickHandler(BaseCommand):
    
    def handle(self, origin, args):
        self._state.change_nick(
            origin,
            parse_numeric(args[0], self._state.max_client_numerics),
            args[1],
            self._state.ts
        )

#
# CAUTION!
#
# Beware's svsnick has a fairly major race condition - N and SN messages
# can cross and there's no way to solve it using the current protocol spec.
#
# The solution is fairly simple, to not actually enact SNs apart from if the
# user is local, and then send an N out as if the user had changed locally.
