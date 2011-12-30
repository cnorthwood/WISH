#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class PasswordHandler(BaseCommand):
    """
    Parses servers being introduced
    """
    
    def __init__(self, state, connection):
        self._connection = connection
        super(PasswordHandler, self).__init__(state)
    
    def handle(self, origin, args):
        self._connection.register_upstream_password(args[-1])
