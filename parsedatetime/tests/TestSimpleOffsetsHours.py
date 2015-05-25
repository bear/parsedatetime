"""
Test parsing of 'simple' offsets
"""

import unittest, time, datetime
import parsedatetime as pdt

class test(unittest.TestCase):

    @pdt.tests.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return pdt.tests.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testHoursFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('5 hours from now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 hour from now',  start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 hr from now',    start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in 5 hours',       start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in 5 hour',        start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 hours',          start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 hr',             start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5h',               start), (target, 2))

        self.assertExpectedResult(self.cal.parse('five hours from now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five hour from now',  start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five hr from now',    start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in five hours',       start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in five hour',        start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five hours',          start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five hr',             start), (target, 2))

        # Test "an"
        t = s + datetime.timedelta(hours=1)
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('an hour from now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in an hour', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('an hour', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('an hr', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('an h', start), (target, 2))

        # No match, should require a word boundary
        self.assertExpectedResult(self.cal.parse('anhour', start), (start, 0))
        self.assertExpectedResult(self.cal.parse('an hamburger', start), (start, 0))

    def testHoursBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(hours=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('5 hours before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 hr before now',    start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5h before now',      start), (target, 2))

        self.assertExpectedResult(self.cal.parse('five hours before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five hr before now',    start), (target, 2))

        # Test "an"
        t = s + datetime.timedelta(hours=-1)
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('an hour before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('an hr before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('an h before now', start), (target, 2))


if __name__ == "__main__":
    unittest.main()
