# -*- coding: utf-8 -*-
"""
Test parsing of strings with multiple chunks
"""
from __future__ import unicode_literals

import sys
import time
import datetime
import parsedatetime as pdt
from . import utils

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class test(unittest.TestCase):

    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return utils.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testSimpleMultipleItems(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3 years 2 weeks 5 days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('3years 2weeks 5days', start), (target, 1))

    def testMultipleItemsSingleCharUnits(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3 y 2 w 5 d', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('3y 2w 5d', start), (target, 1))

        t = self.cal.inc(s, year=3) + datetime.timedelta(hours=5, minutes=50)
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3y 5h 50m', start), (target, 3))

    def testMultipleItemsWithPunctuation(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3 years, 2 weeks, 5 days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('3 years, 2 weeks and 5 days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('3y, 2w, 5d ', start), (target, 1))

    def testUnixATStyle(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=3)

        t = t.replace(hour=16, minute=0, second=0)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('4pm + 3 days', start), (target, 3))
        self.assertExpectedResult(
            self.cal.parse('4pm +3 days', start), (target, 3))

    def testUnixATStyleNegative(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=-3)

        t = t.replace(hour=16, minute=0, second=0)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('4pm - 3 days', start), (target, 3))
        self.assertExpectedResult(
            self.cal.parse('4pm -3 days', start), (target, 3))


if __name__ == "__main__":
    unittest.main()
