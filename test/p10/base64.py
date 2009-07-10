#!/usr/bin/env python

import unittest
import p10.base64

class Base64Test(unittest.TestCase):
    
    def testSingleCharParse(self):
        self.assertEqual(0, p10.base64.toInt('A'))
        self.assertEqual(26, p10.base64.toInt('a'))
        self.assertEqual(63, p10.base64.toInt(']'))
    
    def testRejectInvalidChars(self):
        self.assertRaises(p10.base64.Base64Error, p10.base64.toInt, '#')
    
    def testMultipleCharParse(self):
        self.assertEqual(0, p10.base64.toInt('AA'))
        self.assertEqual(64, p10.base64.toInt('BA'))
        self.assertEqual(90, p10.base64.toInt('Ba'))
        self.assertEqual(127, p10.base64.toInt('B]'))
    
    def testExtendedClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAAAA'))
        self.assertEqual((127, 90), p10.base64.parseNumeric('B]ABa'))
    
    def testExtendedServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parseNumeric('AA'))
        self.assertEqual((127, None), p10.base64.parseNumeric('B]'))
    
    def testShortClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAA'))
        self.assertEqual((2, 90), p10.base64.parseNumeric('CBa'))
    
    def testShortServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parseNumeric('A'))
        self.assertEqual((32, None), p10.base64.parseNumeric('g'))
    
    def testUniversalIRCUNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAAA'))
        self.assertEqual((32, 127), p10.base64.parseNumeric('gAB]'))
    
    def testCreateBase64SingleChar(self):
        self.assertEqual('A', p10.base64.toBase64(0))
        self.assertEqual('a', p10.base64.toBase64(26))
    
    def testCreateBase64MultiChar(self):
        self.assertEqual('BA', p10.base64.toBase64(64))
        self.assertEqual('Ba', p10.base64.toBase64(90))
        self.assertEqual('B]', p10.base64.toBase64(127))
    
    def testCreateClientNumeric(self):
        self.assertEqual('B]BBa', p10.base64.createNumeric((127, 4186)))
    
    def testCreateServerNumeric(self):
        self.assertEqual('BA', p10.base64.createNumeric((64, None)))
    
    def testCreateClientNumericRightLength(self):
        self.assertEqual('AqAB6', p10.base64.createNumeric((42, 122)))
    
    def testCreateServerNumericRightLength(self):
        self.assertEqual('A5', p10.base64.createNumeric((57, None)))


def main():
    unittest.main()

if __name__ == '__main__':
    main()