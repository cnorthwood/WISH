#!/usr/bin/env python

import unittest
import p10.parser

class CommandHandlerDouble():
    
    rcvd = []
    
    def handle(self, origin, line):
        self.rcvd = line

class P10ParserTest(unittest.TestCase):
    
    def testParseSimpleLineSingleArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo\r\n")
        self.assertEquals(['foo'], d.rcvd)
    
    def testParseSimpleLineTwoArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo bar\r\n")
        self.assertEquals(['foo','bar'], d.rcvd)
    
    def testAcceptJustNewLine(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo\n")
        self.assertEquals(['foo'], d.rcvd)
        
    def testRejectBadLineEndings(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser TEST foo")
    
    def testLongArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST :foo bar\r\n")
        self.assertEquals(['foo bar'], d.rcvd)
    
    def testLongArgWithShort(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST baz :foo bar\r\n")
        self.assertEquals(['baz', 'foo bar'], d.rcvd)
    
    def testProtectAgainstLongArgs(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST b:az :foo bar\r\n")
        self.assertEquals(['b:az', 'foo bar'], d.rcvd)
    
    def testRejectUnknownCommands(self):
        p = p10.parser.parser()
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser TEST foo")
    
    def testRejectLongLine(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser TEST baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar\r\n")
    
    def testParseFirstLongArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST baz :foo bar: bar bar foo\r\n")
        self.assertEquals(['baz', 'foo bar: bar bar foo'], d.rcvd)
    
    def testRejectLowercaseCommand(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser test foo\r\n")

def main():
    unittest.main()

if __name__ == '__main__':
    main()