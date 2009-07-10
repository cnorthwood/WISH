#!/usr/bin/env python

import sys
import unittest
import test.p10.parser
import test.p10.base64

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.parser))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.base64))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()