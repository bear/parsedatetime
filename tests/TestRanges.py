# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times
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
        return utils.compareResultByTimeTupleRangesAndFlags(
            result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 14, 0, 0).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.evalRanges(
            "2 pm - 5:30 pm", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "2pm - 5:30pm", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "2:00:00 pm - 5:30:00 pm", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "2 - 5:30pm", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "14:00 - 17:30", start), (targetStart, targetEnd, 2))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 10, 0, 0).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 13, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.evalRanges(
            "10AM - 1:30PM", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "10:00:00 am - 1:30:00 pm", start), (targetStart, targetEnd, 2))
        self.assertExpectedResult(self.cal.evalRanges(
            "10:00 - 13:30", start), (targetStart, targetEnd, 2))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 15, 30, 0).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("today 3:30-5PM", start),
            (targetStart, targetEnd, 2))

    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        targetStart = datetime.datetime(
            2006, 8, 29, self.hr, self.mn, self.sec).timetuple()
        targetEnd = datetime.datetime(
            2006, 9, 2, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("August 29, 2006 - September 2, 2006", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("August 29 - September 2, 2006", start),
            (targetStart, targetEnd, 1))

        targetStart = datetime.datetime(
            2006, 8, 29, self.hr, self.mn, self.sec).timetuple()
        targetEnd = datetime.datetime(
            2006, 9, 2, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("08/29/06 - 09/02/06", start),
            (targetStart, targetEnd, 1))

    def _testSubRanges(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        targetStart = datetime.datetime(2006, 8, 1, 9, 0, 0).timetuple()
        targetEnd = datetime.datetime(2006, 8, 15, 9, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("August 1-15, 2006", start),
            (targetStart, targetEnd, 1))


if __name__ == "__main__":
    unittest.main()
