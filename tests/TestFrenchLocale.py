# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times using the French locale

Note: requires PyICU
"""
from __future__ import unicode_literals
import sys
import time
import datetime
import parsedatetime as pdt
from parsedatetime.pdt_locales import get_icu
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
        locale = 'fr_FR'
        self.ptc = pdt.Constants(locale, usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

        if self.ptc.localeID != locale:
            raise unittest.SkipTest(
                'Locale not set to fr_FR - check if PyICU is installed')

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy,
            self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('2300', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('23:00', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('1100', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('730', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('0730', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('1730', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('173000', start), (target, 2))

    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy,
            self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2006, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('25/08/2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25/8/06', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('août 25, 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('août 25 2006', start), (target, 1))

        if self.mth > 8 or (self.mth == 8 and self.dy > 25):
            target = datetime.datetime(
                self.yr + 1, 8, 25, self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(
                self.yr, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('25/8', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25/08', start), (target, 1))

    def testWeekDays(self):
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
            print(dow)

            result = self.cal.parse(dow, start)

            yr, mth, dy, hr, mn, sec, wd, yd, isdst = result[0]

            self.assertEqual(wd, i)

        self.ptc.CurrentDOWParseStyle = o1
        self.ptc.DOWParseStyle = o2

if __name__ == "__main__":
    unittest.main()
