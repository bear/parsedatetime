# -*- coding: utf-8 -*-
"""
Test parsing of strings that are phrases with the
ptc.StartTimeFromSourceTime flag set to True
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
        self.cal.ptc.StartTimeFromSourceTime = True
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testEndOfPhrases(self):
        s = datetime.datetime.now()

        # find out what month we are currently on
        # set the day to 1 and then go back a day
        # to get the end of the current month
        (yr, mth, dy, hr, mn, sec, _, _, _) = s.timetuple()

        s = datetime.datetime(yr, mth, dy, 13, 14, 15)

        mth += 1
        if mth > 12:
            mth = 1
            yr += 1
        t = datetime.datetime(
            yr, mth, 1, 13, 14, 15) + datetime.timedelta(days=-1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('eom', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('meeting eom', start), (target, 1))

        s = datetime.datetime.now()

        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = s.timetuple()

        s = datetime.datetime(yr, mth, 1, 13, 14, 15)
        t = datetime.datetime(yr, 12, 31, 13, 14, 15)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('eoy', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('meeting eoy', start), (target, 1))
