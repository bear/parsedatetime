# -*- coding: utf-8 -*-
"""
Test parsing of strings that are phrases
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
        # Test with a different day start hour.
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testDifferentDayStartHours(self):
        for day_start_hour in (0, 6, 9, 12):
            cal = pdt.Calendar(day_start_hour=day_start_hour)

            s = datetime.datetime.now()
            t = datetime.datetime(
                self.yr, self.mth, self.dy,
                day_start_hour, 0, 0) + datetime.timedelta(days=1)

            start = s.timetuple()
            target = t.timetuple()

            self.assertExpectedResult(
                cal.parse('tomorrow', start), (target, 1))
            self.assertExpectedResult(
                cal.parse('next day', start), (target, 1))

            t = datetime.datetime(
                self.yr, self.mth, self.dy,
                day_start_hour, 0, 0) + datetime.timedelta(days=-1)
            target = t.timetuple()

            self.assertExpectedResult(
                cal.parse('yesterday', start), (target, 1))

            t = datetime.datetime(
                self.yr, self.mth, self.dy,
                day_start_hour, 0, 0)
            target = t.timetuple()

            self.assertExpectedResult(cal.parse('today', start), (target, 1))
