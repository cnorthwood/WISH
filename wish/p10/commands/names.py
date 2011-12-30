#!/usr/bin/env python

from wish.p10.base64 import parse_numeric
from wish.p10.commands.basecommand import BaseCommand

class NamesHandler(BaseCommand):
    """ Returns users on a channel """
    
    def handle(self, origin, args):
        self._state.request_channel_users(
            origin,
            parse_numeric(args[1], self._state.max_client_numerics),
            args[0].split(",")
        )
