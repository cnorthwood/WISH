#!/usr/bin/env python

import unittest
import test.p10.parser
import test.p10.base64

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.parser))
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.base64))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()