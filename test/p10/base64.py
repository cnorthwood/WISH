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
    
    def testRejectInvalidLength(self):
        self.assertRaises(p10.base64.Base64Error, p10.base64.parseNumeric, 'AAABBB', dict({0: 262143}))
    
    def testMultipleCharParse(self):
        self.assertEqual(0, p10.base64.toInt('AA'))
        self.assertEqual(64, p10.base64.toInt('BA'))
        self.assertEqual(90, p10.base64.toInt('Ba'))
        self.assertEqual(127, p10.base64.toInt('B]'))
    
    def testExtendedClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAAAA', dict({0: 262143})))
        self.assertEqual((127, 90), p10.base64.parseNumeric('B]ABa', dict({127: 262143})))
    
    def testExtendedServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parseNumeric('AA', dict({0: 262143})))
        self.assertEqual((127, None), p10.base64.parseNumeric('B]', dict({127: 262143})))
    
    def testShortClientNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAA', dict({0: 262143})))
        self.assertEqual((2, 90), p10.base64.parseNumeric('CBa', dict({2: 262143})))
    
    def testShortServerNumericParse(self):
        self.assertEqual((0, None), p10.base64.parseNumeric('A', dict({0: 262143})))
        self.assertEqual((32, None), p10.base64.parseNumeric('g', dict({32: 262143})))
    
    def testUniversalIRCUNumericParse(self):
        self.assertEqual((0, 0), p10.base64.parseNumeric('AAAA', dict({0: 262143})))
        self.assertEqual((32, 127), p10.base64.parseNumeric('gAB]', dict({32: 262143})))
    
    def testCreateBase64SingleChar(self):
        self.assertEqual('A', p10.base64.toBase64(0, 0))
        self.assertEqual('a', p10.base64.toBase64(26, 0))
    
    def testCreateBase64MultiChar(self):
        self.assertEqual('BA', p10.base64.toBase64(64, 0))
        self.assertEqual('Ba', p10.base64.toBase64(90, 0))
        self.assertEqual('B]', p10.base64.toBase64(127, 0))
    
    def testCreateClientNumeric(self):
        self.assertEqual('B]BBa', p10.base64.createNumeric((127, 4186)))
    
    def testCreateServerNumeric(self):
        self.assertEqual('BA', p10.base64.createNumeric((64, None)))
    
    def testCreateClientNumericRightLength(self):
        self.assertEqual('AqAB6', p10.base64.createNumeric((42, 122)))
    
    def testCreateServerNumericRightLength(self):
        self.assertEqual('A5', p10.base64.createNumeric((57, None)))
    
    def testMaxNumEquiv(self):
        self.assertEqual(p10.base64.parseNumeric('ABABA', dict({1: 63})), p10.base64.parseNumeric('ABAAA', dict({1: 63})))


def main():
    unittest.main()

if __name__ == '__main__':
    main()