# -*- coding: utf-8 -*-
"""
Test pdtContext
"""

import time
import unittest
import parsedatetime as pdt
from parsedatetime.context import pdtContext


class test(unittest.TestCase):

    def setUp(self):
        self.cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
        (self.yr, self.mth, self.dy, self.hr, self.mn,
         self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def test(self):
        self.assertEqual(self.cal.parse('5 min from now')[1],
                         pdtContext(hasTime=True, hasDate=False))
        self.assertEqual(self.cal.parse('7/11/2015')[1],
                         pdtContext(hasTime=False, hasDate=True))
        self.assertEqual(self.cal.parse('14/32/2015')[1],
                         pdtContext(hasTime=False, hasDate=False))
        self.assertEqual(self.cal.parse('25:23')[1],
                         pdtContext(hasTime=False, hasDate=False))


if __name__ == "__main__":
    unittest.main()
