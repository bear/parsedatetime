"""
Tests the _convertUnitAsWords method.
"""

import sys
import parsedatetime as pdt

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class test(unittest.TestCase):
    def setUp(self):
        self.cal = pdt.Calendar()
        self.tests = (('one', 1),
                      ('zero', 0),
                      ('eleven', 11),
                      ('forty two', 42),
                      ('a hundred', 100),
                      ('four hundred and fifteen', 415),
                      ('twelve thousand twenty', 12020),
                      ('nine hundred and ninety nine', 999),
                      ('three quintillion four billion', 3000000004000000000),
                      ('forty three thousand, nine hundred and ninety nine', 43999),
                      ('one hundred thirty three billion four hundred thousand three hundred fourteen', 133000400314),
                      ('an octillion', 1000000000000000000000000000)
                      )

    def testConversions(self):
        for pair in self.tests:
            self.assertEqual(self.cal._convertUnitAsWords(pair[0]), pair[1])

if __name__ == "__main__":
    unittest.main()
