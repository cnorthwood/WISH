#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand

class EndOfBurstHandler(BaseCommand):
    """
    Parses servers being introduced
    """
    
    def __init__(self, state, connection):
        super(EndOfBurstHandler, self).__init__(state)
        self._connection = connection
    
    def handle(self, origin, args):
        self._connection.register_eob()
