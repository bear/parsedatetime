# -*- coding: utf-8 -*-
"""
Test parsing of units
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

    def testMinutes(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=1)
        h = s - datetime.timedelta(minutes=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 minutes', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1 minute', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1 min', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1min', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1 m', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1m', start), (target, 2))

        self.assertExpectedResult(
            self.cal.parse('1 minutes ago', start), (history, 2))
        self.assertExpectedResult(
            self.cal.parse('1 minute ago', start), (history, 2))

    def testHours(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=1)
        h = s - datetime.timedelta(hours=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 hour', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1 hours', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1 hr', start), (target, 2))

        self.assertExpectedResult(
            self.cal.parse('1 hour ago', start), (history, 2))
        self.assertExpectedResult(
            self.cal.parse('1 hours ago', start), (history, 2))

    def testDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('1 day', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('1 days', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('1days', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('1 dy', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('1 d', start), (target, 1))

    def testNegativeDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=-1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('-1 day', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('-1 days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('-1days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('-1 dy', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('-1 d', start), (target, 1))

        self.assertExpectedResult(
            self.cal.parse('- 1 day', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('- 1 days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('- 1days', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('- 1 dy', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('- 1 d', start), (target, 1))

        self.assertExpectedResult(
            self.cal.parse('1 day ago', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 days ago', start), (target, 1))

    def testWeeks(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)
        h = s - datetime.timedelta(weeks=1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 week', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1week', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 weeks', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 wk', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 w', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1w', start), (target, 1))

        self.assertExpectedResult(
            self.cal.parse('1 week ago', start), (history, 1))
        self.assertExpectedResult(
            self.cal.parse('1 weeks ago', start), (history, 1))

    def testMonths(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, month=1)
        h = self.cal.inc(s, month=-1)

        start = s.timetuple()
        target = t.timetuple()
        history = h.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 month', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 months', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1month', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 month ago', start), (history, 1))
        self.assertExpectedResult(
            self.cal.parse('1 months ago', start), (history, 1))

    def testYears(self):
        s = datetime.datetime.now()
        t = self.cal.inc(s, year=1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('1 year', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 years', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 yr', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1 y', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('1y', start), (target, 1))


if __name__ == "__main__":
    unittest.main()
