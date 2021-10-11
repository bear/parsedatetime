# -*- coding: utf-8 -*-
"""
Test parsing of strings that are phrases
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

    def testPhrases(self):
        #
        # NOTE - this test will fail under certain conditions
        #        It is building an absolute date for comparison and then
        #        testing the parsing of relative phrases and as such will fail
        #        if run near the midnight transition.
        #        Thanks to Chris Petrilli for asking about it and prompting me
        #        to create this note!
        #
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 16, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('flight from SFO at 4pm', start), (target, pdtContext(pdtContext.ACU_HOUR)))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('eod', start), (target, pdtContext(pdtContext.ACU_HALFDAY)))
        self.assertExpectedResult(
            self.cal.parse('meeting eod', start), (target, pdtContext(pdtContext.ACU_HALFDAY)))
        self.assertExpectedResult(
            self.cal.parse('eod meeting', start), (target, pdtContext(pdtContext.ACU_HALFDAY)))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 0, 0) + datetime.timedelta(days=1)
        target = target.timetuple()

        self.assertExpectedResult(
            self.cal.parse('tomorrow eod', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HALFDAY)))
        self.assertExpectedResult(
            self.cal.parse('eod tomorrow', start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HALFDAY)))

    def testPhraseWithDays_DOWStyle_1_False(self):
        s = datetime.datetime.now()

        # find out what day we are currently on
        # and determine what the next day of week is
        t = s + datetime.timedelta(days=1)
        start = s.timetuple()

        (yr, mth, dy, _, _, _, wd, yd, isdst) = t.timetuple()

        target = (yr, mth, dy, 17, 0, 0, wd, yd, isdst)

        d = self.wd + 1
        if d > 6:
            d = 0

        day = self.cal.ptc.Weekdays[d]

        self.assertExpectedResult(
            self.cal.parse('eod %s' % day, start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HALFDAY | pdtContext.ACU_HOUR)))

        # find out what day we are currently on
        # and determine what the previous day of week is
        t = s + datetime.timedelta(days=6)

        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = t.timetuple()

        target = (yr, mth, dy, 17, 0, 0, wd, yd, isdst)

        d = self.wd - 1
        if d < 0:
            d = 6

        day = self.cal.ptc.Weekdays[d]

        self.assertExpectedResult(
            self.cal.parse('eod %s' % day, start), (target, pdtContext(pdtContext.ACU_DAY | pdtContext.ACU_HALFDAY | pdtContext.ACU_HOUR)))

    def testEndOfPhrases(self):
        s = datetime.datetime.now()

        # find out what month we are currently on
        # set the day to 1 and then go back a day
        # to get the end of the current month
        (yr, mth, _, hr, mn, sec, _, _, _) = s.timetuple()

        mth += 1
        if mth > 12:
            mth = 1
            yr += 1

        t = datetime.datetime(
            yr, mth, 1, 9, 0, 0) + datetime.timedelta(days=-1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('eom', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('meeting eom', start), (target, pdtContext(pdtContext.ACU_DAY)))

        s = datetime.datetime.now()

        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = s.timetuple()

        t = datetime.datetime(yr, 12, 31, 9, 0, 0)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('eoy', start), (target, pdtContext(pdtContext.ACU_MONTH)))
        self.assertExpectedResult(
            self.cal.parse('meeting eoy', start), (target, pdtContext(pdtContext.ACU_MONTH)))

    def testLastPhrases(self):
        for day in (11, 12, 13, 14, 15, 16, 17):
            start = datetime.datetime(2012, 11, day, 9, 0, 0)

            (yr, mth, dy, _, _, _, wd, yd, isdst) = start.timetuple()

            n = 4 - wd
            if n >= 0:
                n -= 7

            target = start + datetime.timedelta(days=n)

            self.assertExpectedResult(
                self.cal.parse('last friday', start.timetuple()),
                (target.timetuple(), pdtContext(pdtContext.ACU_DAY)), dateOnly=True)
