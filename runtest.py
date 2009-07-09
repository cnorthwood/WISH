#!/usr/bin/env python

import unittest
import test.p10.parser

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromModule(test.p10.parser))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()