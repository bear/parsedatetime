# -*- coding: utf-8 -*-
"""
Test parsing of complex date and times
"""
import sys
import time
from datetime import datetime
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

    def testDate3ConfusedHourAndYear(self):
        ctx = pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)
        start = datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('Aug 05, 2014 4:15 AM'),
            (datetime(2014, 8, 5, 4, 15, 0).timetuple(),
            pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('Aug 05, 2003 3:15 AM'),
            (datetime(2003, 8, 5, 3, 15, 0).timetuple(),
            pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('Aug 05, 2003 03:15 AM'),
            (datetime(2003, 8, 5, 3, 15, 0).timetuple(),
            pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('June 30th 12PM', start),
            (datetime(self.yr
                      if datetime.now() < datetime(self.yr, 6, 30, 12)
                      else self.yr + 1,
                      6, 30, 12, 0, 0).timetuple(), 
                      pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('June 30th 12:00', start),
            (datetime(self.yr
                      if datetime.now() < datetime(self.yr, 6, 30, 12)
                      else self.yr + 1,
                      6, 30, 12, 0, 0).timetuple(),
                      pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('December 30th 23PM', start),
            (datetime(self.yr
                      if datetime.now() < datetime(self.yr, 12, 30, 23)
                      else self.yr + 1,
                      12, 30, 23, 0, 0).timetuple(),
                      pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('December 30th 23:02', start),
            (datetime(self.yr
                      if datetime.now() < datetime(self.yr, 12, 30, 23, 2)
                      else self.yr + 1,
                      12, 30, 23, 2, 0).timetuple(),
                      pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

    def testDates(self):
        start = datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime(2006, 8, 25, 17, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('08/25/2006 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm on 08.25.2006', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm August 25, 2006', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm August 25th, 2006', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm 25 August, 2006', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm 25th August, 2006', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('Aug 25, 2006 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('Aug 25th, 2006 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('25 Aug, 2006 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('25th Aug 2006, 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))

        if self.mth > 8 or (self.mth == 8 and self.dy > 5):
            target = datetime(self.yr + 1, 8, 5, 17, 0, 0).timetuple()
        else:
            target = datetime(self.yr, 8, 5, 17, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('8/5 at 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm 8.5', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('08/05 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('August 5 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm Aug 05', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('Aug 05 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('Aug 05th 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5 August 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5th August 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('5pm 05 Aug', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('05 Aug 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('05th Aug 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('August 5th 5pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))

        if self.mth > 8 or (self.mth == 8 and self.dy > 5):
            target = datetime(self.yr + 1, 8, 5, 12, 0, 0).timetuple()
        else:
            target = datetime(self.yr, 8, 5, 12, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('August 5th 12:00', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('August 5th 12pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('August 5th 12:00pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('August 5th 12 pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))
        self.assertExpectedResult(
            self.cal.parse('August 5th 12:00 pm', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

        if self.mth > 8 or (self.mth == 8 and self.dy > 22):
            target = datetime(
                self.yr + 1, 8, 22, 3, 26, 0).timetuple()
        else:
            target = datetime(self.yr, 8, 22, 3, 26, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('August 22nd 3:26', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('August 22nd 3:26am', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))
        self.assertExpectedResult(
            self.cal.parse('August 22nd 3:26 am', start),
            (target, pdtContext(pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR | pdtContext.ACU_MIN)))

    def testDatesWithDay(self):
        start = datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime(2016, 8, 23, 17, 0, 0).timetuple()
        self.assertExpectedResult(
            self.cal.parse('tuesday august 23nd 2016 at 5pm', start),
            (target, pdtContext(pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY | pdtContext.ACU_HOUR)))


if __name__ == "__main__":
    unittest.main()
