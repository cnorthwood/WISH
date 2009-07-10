#!/usr/bin/env python

import unittest
import p10.base64

class Base64Test(unittest.TestCase):
    
    def testSingleCharParse(self):
        self.assertEqual(0, p10.base64.toint('A'))
        self.assertEqual(26, p10.base64.toint('a'))
        self.assertEqual(63, p10.base64.toint(']'))
    
    def testRejectInvalidChars(self):
        self.assertRaises(p10.base64.Base64Error, p10.base64.toint, '#')
    
    def testMultipleCharParse(self):
        self.assertEqual(0, p10.base64.toint('AA'))
        self.assertEqual(64, p10.base64.toint('BA'))
        self.assertEqual(90, p10.base64.toint('Ba'))
        self.assertEqual(127, p10.base64.toint('B]'))
    
    def testExtendedClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parsenumeric('AAAAA'))
        self.assertEqual((127, 90), p10.base64.parsenumeric('B]ABa'))
    
    def testExtendedServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parsenumeric('AA'))
        self.assertEqual((127, None), p10.base64.parsenumeric('B]'))
    
    def testShortClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parsenumeric('AAA'))
        self.assertEqual((2, 90), p10.base64.parsenumeric('CBa'))
    
    def testShortServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parsenumeric('A'))
        self.assertEqual((32, None), p10.base64.parsenumeric('g'))
    
    def testUniversalIRCUNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parsenumeric('AAAA'))
        self.assertEqual((32, 127), p10.base64.parsenumeric('gAB]'))
    
    def testCreateBase64SingleChar(self):
        self.assertEqual('A', p10.base64.tobase64(0))
        self.assertEqual('a', p10.base64.tobase64(26))
    
    def testCreateBase64MultiChar(self):
        self.assertEqual('BA', p10.base64.tobase64(64))
        self.assertEqual('Ba', p10.base64.tobase64(90))
        self.assertEqual('B]', p10.base64.tobase64(127))
    
    def testCreateClientNumeric(self):
        self.assertEqual('B]BBa', p10.base64.createnumeric((127, 4186)))
    
    def testCreateServerNumeric(self):
        self.assertEqual('BA', p10.base64.createnumeric((64, None)))
    
    def testCreateClientNumericRightLength(self):
        self.assertEqual('AqAB6', p10.base64.createnumeric((42, 122)))
    
    def testCreateServerNumericRightLength(self):
        self.assertEqual('A5', p10.base64.createnumeric((57, None)))


def main():
    unittest.main()

if __name__ == '__main__':
    main()