#!/usr/bin/env python

import sys
import unittest
import test.p10.parser
import test.p10.base64
import test.p10.state
import test.p10.commands.account
import test.p10.commands.admin

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.parser))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.base64))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.state))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.account))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.commands.admin))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()