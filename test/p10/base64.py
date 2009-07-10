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


def main():
    unittest.main()

if __name__ == '__main__':
    main()