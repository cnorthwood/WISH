#!/usr/bin/env python

import unittest
import p10.parser

class CommandHandlerDouble():
    
    rcvd = []
    
    def handle(origin, line):
        rcvd = line

class P10ParserTest(unittest.TestCase):
    
    def testParseSimpleLine(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo\r\n")
        self.assertEquals(['foo'], d.rcvd)

def main():
    unittest.main()

if __name__ == '__main__':
    main()