#!/usr/bin/env python

import unittest
import p10.connection

class TestableConnection(p10.connection.connection):
    insight = []
    def __init__(self, state):
        self.insight = []
    def _sendLine(self, origin, command, args):
        self.insight.append(self._parser.build(source_client, token, args))

class StateDouble:
    maxClientNumerics = dict({1: 262143})
    pass

class ConnectionTest(unittest.TestCase):
    pass

def main():
    unittest.main()

if __name__ == '__main__':
    main()