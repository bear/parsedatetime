# -*- coding: utf-8 -*-
"""
Test parsing of units
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

    def testMinutes(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=1)
        h = s - datetime.timedelta(minutes=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 minutes', start),
            (target, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1 minute', start),
            (target, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1 min', start),
            (target, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1min', start),
            (target, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1 m', start),
            (target, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1m', start),
            (target, pdtContext(pdtContext.ACU_MIN)))

        self.assertExpectedResult(
            self.cal.parse('1 minutes ago', start),
            (history, pdtContext(pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('1 minute ago', start),
            (history, pdtContext(pdtContext.ACU_MIN)))

    def testHours(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=1)
        h = s - datetime.timedelta(hours=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 hour', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('1 hours', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('1 hr', start),
            (target, pdtContext(pdtContext.ACU_HOUR)))

        self.assertExpectedResult(
            self.cal.parse('1 hour ago', start),
            (history, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('1 hours ago', start),
            (history, pdtContext(pdtContext.ACU_HOUR)))

    def testDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 day', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('1 days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('1days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('1 dy', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('1 d', start),
            (target, pdtContext(pdtContext.ACU_DAY)))

    def testNegativeDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=-1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('-1 day', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('-1 days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('-1days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('-1 dy', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('-1 d', start),
            (target, pdtContext(pdtContext.ACU_DAY)))

        self.assertExpectedResult(
            self.cal.parse('- 1 day', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('- 1 days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('- 1days', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('- 1 dy', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('- 1 d', start),
            (target, pdtContext(pdtContext.ACU_DAY)))

        self.assertExpectedResult(
            self.cal.parse('1 day ago', start),
            (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('1 days ago', start),
            (target, pdtContext(pdtContext.ACU_DAY)))

    def testWeeks(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)
        h = s - datetime.timedelta(weeks=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 week', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1week', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1 weeks', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1 wk', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1 w', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1w', start),
            (target, pdtContext(pdtContext.ACU_WEEK)))

        self.assertExpectedResult(
            self.cal.parse('1 week ago', start),
            (history, pdtContext(pdtContext.ACU_WEEK)))
        self.assertExpectedResult(
            self.cal.parse('1 weeks ago', start),
            (history, pdtContext(pdtContext.ACU_WEEK)))

    def testMonths(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, month=1)
        h = self.cal.inc(s, month=-1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 month', start),
            (target, pdtContext(pdtContext.ACU_MONTH)))
        self.assertExpectedResult(
            self.cal.parse('1 months', start),
            (target, pdtContext(pdtContext.ACU_MONTH)))
        self.assertExpectedResult(
            self.cal.parse('1month', start),
            (target, pdtContext(pdtContext.ACU_MONTH)))

        self.assertExpectedResult(
            self.cal.parse('1 month ago', start),
            (history, pdtContext(pdtContext.ACU_MONTH)))
        self.assertExpectedResult(
            self.cal.parse('1 months ago', start),
            (history, pdtContext(pdtContext.ACU_MONTH)))

    def testYears(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 year', start),
            (target, pdtContext(pdtContext.ACU_YEAR)))
        self.assertExpectedResult(
            self.cal.parse('1 years', start),
            (target, pdtContext(pdtContext.ACU_YEAR)))
        self.assertExpectedResult(
            self.cal.parse('1 yr', start),
            (target, pdtContext(pdtContext.ACU_YEAR)))
        self.assertExpectedResult(
            self.cal.parse('1 y', start),
            (target, pdtContext(pdtContext.ACU_YEAR)))
        self.assertExpectedResult(
            self.cal.parse('1y', start),
            (target, pdtContext(pdtContext.ACU_YEAR)))


if __name__ == "__main__":
    unittest.main()
