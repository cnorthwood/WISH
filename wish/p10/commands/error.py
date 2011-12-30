#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.errors import ConnectionError

class ErrorHandler(BaseCommand):
    """
    Parses errors sent on-link
    """
    
    def handle(self, origin, line):
        raise ConnectionError(
            "Error received from upstream server: " + line[-1]
        )
