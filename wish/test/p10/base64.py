#!/usr/bin/env python

import unittest
from wish.p10.base64 import parse_numeric, to_int, to_base64, Base64Error, create_numeric

class Base64Test(unittest.TestCase):
    
    def testSingleCharParse(self):
        self.assertEqual(0, to_int('A'))
        self.assertEqual(26, to_int('a'))
        self.assertEqual(63, to_int(']'))
    
    def testRejectInvalidChars(self):
        self.assertRaises(Base64Error, to_int, '#')
    
    def testRejectInvalidLength(self):
        self.assertRaises(Base64Error, parse_numeric, 'AAABBB', dict({0: 262143}))
    
    def testMultipleCharParse(self):
        self.assertEqual(0, to_int('AA'))
        self.assertEqual(64, to_int('BA'))
        self.assertEqual(90, to_int('Ba'))
        self.assertEqual(127, to_int('B]'))
    
    def testExtendedClientNumericParse(self):
        self.assertEqual((0, 0), parse_numeric('AAAAA', dict({0: 262143})))
        self.assertEqual((127, 90), parse_numeric('B]ABa', dict({127: 262143})))
    
    def testExtendedServerNumericParse(self):
        self.assertEqual((0, None), parse_numeric('AA', dict({0: 262143})))
        self.assertEqual((127, None), parse_numeric('B]', dict({127: 262143})))
    
    def testShortClientNumericParse(self):
        self.assertEqual((0, 0), parse_numeric('AAA', dict({0: 262143})))
        self.assertEqual((2, 90), parse_numeric('CBa', dict({2: 262143})))
    
    def testShortServerNumericParse(self):
        self.assertEqual((0, None), parse_numeric('A', dict({0: 262143})))
        self.assertEqual((32, None), parse_numeric('g', dict({32: 262143})))
    
    def testUniversalIRCUNumericParse(self):
        self.assertEqual((0, 0), parse_numeric('AAAA', dict({0: 262143})))
        self.assertEqual((32, 127), parse_numeric('gAB]', dict({32: 262143})))
    
    def testCreateBase64SingleChar(self):
        self.assertEqual('A', to_base64(0, 0))
        self.assertEqual('a', to_base64(26, 0))
    
    def testCreateBase64MultiChar(self):
        self.assertEqual('BA', to_base64(64, 0))
        self.assertEqual('Ba', to_base64(90, 0))
        self.assertEqual('B]', to_base64(127, 0))
    
    def testCreateClientNumeric(self):
        self.assertEqual('B]BBa', create_numeric((127, 4186)))
    
    def testCreateServerNumeric(self):
        self.assertEqual('BA', create_numeric((64, None)))
    
    def testCreateClientNumericRightLength(self):
        self.assertEqual('AqAB6', create_numeric((42, 122)))
    
    def testCreateServerNumericRightLength(self):
        self.assertEqual('A5', create_numeric((57, None)))
    
    def testMaxNumEquiv(self):
        self.assertEqual(parse_numeric('ABABA', dict({1: 63})), parse_numeric('ABAAA', dict({1: 63})))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
