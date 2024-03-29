# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times using the Australian locale
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
        self.ptc = pdt.Constants('en_AU', usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

        if self.ptc.localeID != 'en_AU':
            raise unittest.SkipTest(
                'Locale not set to en_AU - check if PyICU is installed')

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('11:00:00 PM', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN | pdtContext.ACU_SEC)))
        self.assertExpectedResult(
            self.cal.parse('11:00 PM', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('11 PM', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('11PM', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('2300', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('23:00', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('11p', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('11pm', start), (target, pdtContext(pdtContext.ACU_HOUR)))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('11:00:00 AM', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN | pdtContext.ACU_SEC)))
        self.assertExpectedResult(
            self.cal.parse('11:00 AM', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('11 AM', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('11AM', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('1100', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('11:00', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('11a', start), (target, pdtContext(pdtContext.ACU_HOUR)))
        self.assertExpectedResult(self.cal.parse('11am', start), (target, pdtContext(pdtContext.ACU_HOUR)))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('0730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('1730', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(self.cal.parse('173000', start), (target, pdtContext(pdtContext.ACU_HOUR | pdtContext.ACU_MIN | pdtContext.ACU_SEC)))

    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2006, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('25-08-2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('25/08/2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('25.08.2006', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('25-8-06', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(
            self.cal.parse('25/8/06', start), (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))

        if self.mth > 8 or (self.mth == 8 and self.dy > 25):
            target = datetime.datetime(
                self.yr + 1, 8, 25, self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(
                self.yr, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(self.cal.parse('25/8', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('25.8', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('25-08', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('25/08', start), (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY)))


if __name__ == "__main__":
    unittest.main()
