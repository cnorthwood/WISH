#!/usr/bin/env python

import unittest
import p10.commands.error
import p10.connection

class StateDouble:
    pass

class ErrorTest(unittest.TestCase):
    
    def testErrorRaised(self):
        s = StateDouble()
        c = p10.commands.error.error(s)
        self.assertRaises(p10.connection.ConnectionError, c.handle, (1, None), ["An error has occured"])
    
    # No further unit tests required here - covered by test.p10.state

def main():
    unittest.main()

if __name__ == '__main__':
    main()