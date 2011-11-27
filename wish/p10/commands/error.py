#!/usr/bin/env python

import genericcommand
import p10.connection

class error(genericcommand.genericcommand):
    """ Parses errors sent on-link """
    
    def handle(self, origin, line):
        raise p10.connection.ConnectionError("Error received from upstream server: " + line[-1])