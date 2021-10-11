# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times using the French locale

Note: requires PyICU
"""
import sys
import time
import datetime
import unittest
import pytest
import parsedatetime as pdt
from parsedatetime.context import pdtContext
from . import utils


class test(unittest.TestCase):

    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return utils.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.ptc = pdt.Constants('fr_FR')
        self.cal = pdt.Calendar(self.ptc)

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testTimes(self):
        if self.ptc.localeID == 'fr_FR':
            start = datetime.datetime(
                self.yr, self.mth, self.dy,
                self.hr, self.mn, self.sec).timetuple()
            target = datetime.datetime(
                self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

            self.assertExpectedResult(
                self.cal.parse('2300', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
            self.assertExpectedResult(
                self.cal.parse('23:00', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

            target = datetime.datetime(
                self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

            self.assertExpectedResult(
                self.cal.parse('1100', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
            self.assertExpectedResult(
                self.cal.parse('11:00', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

            target = datetime.datetime(
                self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

            self.assertExpectedResult(
                self.cal.parse('730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
            self.assertExpectedResult(
                self.cal.parse('0730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

            target = datetime.datetime(
                self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

            self.assertExpectedResult(
                self.cal.parse('1730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
            self.assertExpectedResult(
                self.cal.parse('173000', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN | pdtContext.ACU_SEC)))

    def testDates(self):
        if self.ptc.localeID == 'fr_FR':
            start = datetime.datetime(
                self.yr, self.mth, self.dy,
                self.hr, self.mn, self.sec).timetuple()
            target = datetime.datetime(
                2006, 8, 25, self.hr, self.mn, self.sec).timetuple()

            self.assertExpectedResult(
                self.cal.parse('25/08/2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
            self.assertExpectedResult(
                self.cal.parse('25/8/06', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
            self.assertExpectedResult(
                self.cal.parse('août 25, 2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
            self.assertExpectedResult(
                self.cal.parse('août 25 2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))

            if self.mth > 8 or (self.mth == 8 and self.dy > 25):
                target = datetime.datetime(
                    self.yr + 1, 8, 25, self.hr, self.mn, self.sec).timetuple()
            else:
                target = datetime.datetime(
                    self.yr, 8, 25, self.hr, self.mn, self.sec).timetuple()

            self.assertExpectedResult(
                self.cal.parse('25/8', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
            self.assertExpectedResult(
                self.cal.parse('25/08', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))

    def testWeekDays(self):
        if self.ptc.localeID == 'fr_FR':
            start = datetime.datetime(
                self.yr, self.mth, self.dy,
                self.hr, self.mn, self.sec).timetuple()

            o1 = self.ptc.CurrentDOWParseStyle
            o2 = self.ptc.DOWParseStyle

            # set it up so the current dow returns current day
            self.ptc.CurrentDOWParseStyle = True
            self.ptc.DOWParseStyle = 1

            for i in range(0, 7):
                dow = self.ptc.shortWeekdays[i]

                result = self.cal.parse(dow, start)

                yr, mth, dy, hr, mn, sec, wd, yd, isdst = result[0]

                self.assertEqual(wd, i)

            self.ptc.CurrentDOWParseStyle = o1
            self.ptc.DOWParseStyle = o2


class TestDayOffsets(test):
    # test how Aujourd'hui/Demain/Hier are parsed

    def setUp(self):
        super(TestDayOffsets, self).setUp()
        self.ptc = pdt.Constants('fr_FR', usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)

    def test_dayoffsets(self):
        start = datetime.datetime(self.yr, self.mth, self.dy, 9)
        for date_string, expected_day_offset in [
                ("Aujourd'hui", 0),
                ("aujourd'hui", 0),
                ("Demain", 1),
                ("demain", 1),
                ("Hier", -1),
                ("hier", -1),
                ("au jour de hui", None)]:
            got_dt, rc = self.cal.parseDT(date_string, start)
            if expected_day_offset is not None:
                self.assertEqual(rc, pdtContext(pdtContext.ACU_DAY))
                target = (start + datetime.timedelta(days=expected_day_offset))
                self.assertEqual(got_dt, target)
            else:
                self.assertEqual(rc, pdtContext())


if __name__ == "__main__":
    unittest.main()
