# -*- coding: utf-8 -*-
"""
Test parsing of 'simple' offsets
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

    def testHoursFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=5)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('5 hours from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('5 hour from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('5 hr from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('in 5 hours', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('in 5 hour', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5 hours', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('5 hr', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('5h', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))

        self.assertExpectedResult(
            self.cal.parse('five hours from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('five hour from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('five hr from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('in five hours', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('in five hour', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('five hours', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('five hr', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))

        # Test "an"
        t = s + datetime.timedelta(hours=1)
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('an hour from now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('in an hour', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('an hour', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('an hr', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('an h', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))

        # No match, should require a word boundary
        self.assertExpectedResult(
            self.cal.parse('anhour', start),
            (start, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('an hamburger', start),
            (start, pdtContext()))

    def testHoursBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=-5)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('5 hours before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('5 hr before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('5h before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))

        self.assertExpectedResult(
            self.cal.parse('five hours before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('five hr before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))

        # Test "an"
        t = s + datetime.timedelta(hours=-1)
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('an hour before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('an hr before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))
        self.assertExpectedResult(
            self.cal.parse('an h before now', start),
            (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_NOW)))


if __name__ == "__main__":
    unittest.main()
