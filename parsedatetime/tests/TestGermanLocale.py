
"""
Test parsing of simple date and times using the German locale
"""

import unittest, time, datetime
import parsedatetime as pdt


class test(unittest.TestCase):

    @pdt.tests.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return pdt.tests.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.ptc = pdt.Constants('de_DE', usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)

        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

        if self.ptc.localeID != 'de_DE':
            raise unittest.SkipTest('Locale not set to de_DE - check if PyICU is installed')

    def testTimes(self):
        start  = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('23:00:00', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('23:00',    start), (target, 2))
        self.assertExpectedResult(self.cal.parse('2300',     start), (target, 2))

        target = datetime.datetime(self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('11:00:00', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('11:00',    start), (target, 2))
        self.assertExpectedResult(self.cal.parse('1100',     start), (target, 2))

        target = datetime.datetime(self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('730',  start), (target, 2))
        self.assertExpectedResult(self.cal.parse('0730', start), (target, 2))

        target = datetime.datetime(self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('1730',   start), (target, 2))
        self.assertExpectedResult(self.cal.parse('173000', start), (target, 2))

    def testDates(self):
        start  = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(2006, 8, 25,  self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(self.cal.parse('25.08.2006', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('25.8.06',    start), (target, 1))

        if self.mth > 8 or (self.mth == 8 and self.dy > 25):
            target = datetime.datetime(self.yr+1, 8, 25,  self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(self.yr, 8, 25,  self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(self.cal.parse('25.8',       start), (target, 1))
        self.assertExpectedResult(self.cal.parse('25.08',      start), (target, 1))


if __name__ == "__main__":
    unittest.main()
