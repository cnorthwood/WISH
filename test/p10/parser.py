#!/usr/bin/env python

import unittest
import p10.parser

class CommandHandlerDouble():
    
    rcvd = []
    origin = None
    
    def handle(self, origin, line):
        self.rcvd = line
        self.origin = origin

class P10ParserTest(unittest.TestCase):
    
    def testParseSimpleLineSingleArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo\r\n")
        self.assertEquals(['foo'], d.rcvd)
    
    def testBuildSimpleLineSingleArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST foo\r\n", p.build((1,1), "TEST", ['foo']))
        
    def testParseSimpleLineTwoArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST foo bar\r\n")
        self.assertEquals(['foo','bar'], d.rcvd)
        
    def testBuildSimpleLineTwoArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST foo bar\r\n", p.build((1,1), "TEST", ['foo','bar']))
    
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
    
    def testBuildLongArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST :foo bar\r\n", p.build((1,1), "TEST", ['foo bar']))
    
    def testLongArgWithShort(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST baz :foo bar\r\n")
        self.assertEquals(['baz', 'foo bar'], d.rcvd)
    
    def testBuildLongArgWithShort(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST baz :foo bar\r\n", p.build((1,1), "TEST", ['baz', 'foo bar']))
    
    def testProtectAgainstLongArgs(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST b:az :foo bar\r\n")
        self.assertEquals(['b:az', 'foo bar'], d.rcvd)
    
    def testProtectAgainstLongArgsInBuild(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST b:az :foo bar\r\n", p.build((1,1), "TEST", ['b:az', 'foo bar']))
    
    def testRejectUnknownCommands(self):
        p = p10.parser.parser()
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser TEST foo\r\n")
    
    def testNoBuildUnknownCommands(self):
        p = p10.parser.parser()
        self.assertRaises(p10.parser.ParseError, p.build, (1,1), "TEST", ["foo"])
    
    def testRejectLongLine(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser TEST baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar\r\n")
    
    def testNoBuildLongLine(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.build, (1,1), "TEST", ["baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar baz foo bar"])
    
    def testParseFirstLongArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse(":testuser TEST baz :foo bar: bar bar foo\r\n")
        self.assertEquals(['baz', 'foo bar: bar bar foo'], d.rcvd)
        
    def testBuildFirstLongArg(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("ABAAB TEST baz :foo bar: bar bar foo\r\n", p.build((1,1), "TEST", ['baz', 'foo bar: bar bar foo']))
        
    def testRejectLowercaseCommand(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertRaises(p10.parser.ParseError, p.parse, ":testuser test foo\r\n")
        
    def testNoLowercaseCommand(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        self.assertRaises(p10.parser.ParseError, p.build, (1,1), "test", ["foo"])
    
    def testOriginSetCorrectly(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse("ABAAB TEST baz\r\n")
        self.assertEquals((1,1), d.origin)
    
    def testOriginSetCorrectlyServerOnly(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.parse("AB TEST baz\r\n")
        self.assertEquals((1,None), d.origin)
    
    def testOriginBuildCorrectlyServerOnly(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        self.assertEquals("AB TEST baz\r\n", p.build((1,None), "TEST", ["baz"]))
    
    def testBuildPropagatesChangesToState(self):
        p = p10.parser.parser()
        d = CommandHandlerDouble()
        p.registerHandler("TEST", d)
        p.build((1,1), "TEST", ["baz","foo bar"])
        self.assertEquals((1,1), d.origin)
        self.assertEquals(['baz', 'foo bar'], d.rcvd)

def main():
    unittest.main()

if __name__ == '__main__':
    main()