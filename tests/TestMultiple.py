# -*- coding: utf-8 -*-
"""
Test parsing of strings with multiple chunks
"""
import sys
import time
import datetime
import unittest
import parsedatetime as pdt
from parsedatetime.context import pdtContext
from . import utils


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
            self.cal.parse('3 years 2 weeks 5 days', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('3years 2weeks 5days', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))

    def testMultipleItemsSingleCharUnits(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3 y 2 w 5 d', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('3y 2w 5d', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))

        t = self.cal.inc(s, year=3) + datetime.timedelta(hours=5, minutes=50)
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3y 5h 50m', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

    def testMultipleItemsWithPunctuation(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=3) + datetime.timedelta(days=5, weeks=2)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('3 years, 2 weeks, 5 days', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('3 years, 2 weeks and 5 days', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('3y, 2w, 5d ', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_WEEK | pdtContext.ACU_DAY)))

    def testUnixATStyle(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=3)

        t = t.replace(hour=16, minute=0, second=0)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('4pm + 3 days', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('4pm +3 days', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))

    def testUnixATStyleNegative(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=-3)

        t = t.replace(hour=16, minute=0, second=0)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('4pm - 3 days', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('4pm -3 days', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))


if __name__ == "__main__":
    unittest.main()
