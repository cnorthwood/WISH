#!/usr/bin/env python

from wish.p10.commands.basecommand import BaseCommand
from wish.p10.base64 import parse_numeric

class NumberRelayHandler(BaseCommand):
    
    def __init__(self, state, number):
        self._number = number
        super(NumberRelayHandler, self).__init__(state)
    
    def handle(self, origin, args):
        self._state.oobmsg(origin, self._number, args)
