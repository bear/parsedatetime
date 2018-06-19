# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times
"""
from __future__ import unicode_literals

import sys
import time
import datetime
import parsedatetime as pdt

import utils

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
            "10:00:00 - 13:30:00", start), (targetStart, targetEnd, 2))
        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 15, 0, 0).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("today 3-5:30 pm", start),
            (targetStart, targetEnd, 2))
        self.assertExpectedResult(
            self.cal.evalRanges("15:00 - 17:30", start),
            (targetStart, targetEnd, 2))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 15, 45, 0).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("today 3:45-5 pm", start),
            (targetStart, targetEnd, 2))

        self.assertExpectedResult(
            self.cal.evalRanges("today 3:45-5:00 PM", start),
            (targetStart, targetEnd, 2))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 16, 0, 55).timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 44).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("4:00:55 pm - 5:30:44 pm", start),
            (targetStart, targetEnd, 2))


    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()

        targetStart = datetime.datetime(
            2006, 8, 29, self.hr, self.mn, self.sec).timetuple()
        targetEnd = datetime.datetime(
            2006, 9, 2, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("Aug 29, 2006 - Sep 2, 2006", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("August 29 - September 2 2006", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("29 August- 2 September 2006", start),
            (targetStart, targetEnd, 1))
        '''self.assertExpectedResult(
            self.cal.evalRanges("August 29th - September 2nd, 2006", start),
            (targetStart, targetEnd, 1))'''

        targetStart = datetime.datetime(
            self.yr + 1, 3, 2, self.hr, self.mn, self.sec).timetuple()
        targetEnd = datetime.datetime(
            self.yr + 1, 3, 13, self.hr, self.mn, self.sec).timetuple()
        # +1 is added to the year because march of this year is over, therefore will go one to next year
        self.assertExpectedResult(
            self.cal.evalRanges(" Mar 2nd - 13th", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("2 - 13 March", start),
            (targetStart, targetEnd, 1))

        targetStart = datetime.datetime(
            2006, 8, 29, self.hr, self.mn, self.sec).timetuple()
        targetEnd = datetime.datetime(
            2006, 9, 2, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.evalRanges("08/29/06 - 09/02/2006", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("2006/8/29 - 2006/9/2", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("2006/08/29 - 2006/09/02", start),
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
