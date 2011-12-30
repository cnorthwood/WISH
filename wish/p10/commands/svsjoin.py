#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class SvsJoinHandler(BaseCommand):
    
    def handle(self, origin, args):
        target = parse_numeric(args[0], self._state.max_client_numerics)
        for channel in args[1].split(","):
            self._state.join_channel(origin, target, channel, [])

#
# Caution!
#
# svsjoin's as defined in Beware's spec have race conditions - the solution is
# the same as for SVSNICK, simply propogate the message to the target and then
# the target server sends a join out as per usual.
