#!/usr/bin/env python

from wish.p10.base64 import parse_numeric
from wish.p10.commands.basecommand import BaseCommand

class AccountHandler(BaseCommand):
    """
    Parses the AC/ACCOUNT token - users authenticating
    """
    
    def handle(self, origin, line):
        self._state.authenticate(
            origin,
            parse_numeric(line[0], self._state.max_client_numerics),
            line[1]
        )
