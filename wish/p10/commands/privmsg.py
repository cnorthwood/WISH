#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric, Base64Error

class PrivmsgHandler(BaseCommand):
    
    def handle(self, origin, args):
        try:
            target = parse_numeric(args[0], self._state.max_client_numerics)
        except Base64Error:
            target = args[0]
        self._state.privmsg(origin, target, args[-1])
