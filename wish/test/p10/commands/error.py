#!/usr/bin/env python

import unittest

from wish.p10.commands.error import ErrorHandler
from wish.p10.connection import ConnectionError

class StateDouble():
    pass


class ErrorTest(unittest.TestCase):
    
    def testErrorRaised(self):
        s = StateDouble()
        c = ErrorHandler(s)
        self.assertRaises(ConnectionError, c.handle, (1, None), ["An error has occured"])
    
    # No further unit tests required here - covered by test.p10.state


def main():
    unittest.main()

if __name__ == '__main__':
    main()
