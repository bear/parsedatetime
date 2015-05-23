
"""
Test parsing of units
"""

import unittest, time, datetime
import parsedatetime as pdt

class test(unittest.TestCase):

    @pdt.tests.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return pdt.tests.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    @pdt.tests.assertEqualWithComparator
    def assertExpectedErrorFlag(self, result, check, **kwargs):
        return pdt.tests.compareResultByFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testErrors(self):
        s     = datetime.datetime.now()
        start = s.timetuple()

        # These tests all return current date/time as they are out of range
        self.assertExpectedResult(self.cal.parse('01/0',   start), (start, 0))
        self.assertExpectedResult(self.cal.parse('08/35',  start), (start, 0))
        self.assertExpectedResult(self.cal.parse('18/35',  start), (start, 0))
        self.assertExpectedResult(self.cal.parse('1799',   start), (start, 0))
        self.assertExpectedResult(self.cal.parse('781',    start), (start, 0))
        self.assertExpectedResult(self.cal.parse('2702',   start), (start, 0))
        self.assertExpectedResult(self.cal.parse('78',     start), (start, 0))
        self.assertExpectedResult(self.cal.parse('11',     start), (start, 0))
        self.assertExpectedResult(self.cal.parse('1',      start), (start, 0))
        self.assertExpectedResult(self.cal.parse('174565', start), (start, 0))
        self.assertExpectedResult(self.cal.parse('177505', start), (start, 0))
        # ensure short month names do not cause false positives within a word - jun (june)
        self.assertExpectedResult(self.cal.parse('injunction', start), (start, 0))
        # ensure short month names do not cause false positives at the start of a word - jul (juuly)
        self.assertExpectedResult(self.cal.parse('julius', start), (start, 0))
        # ensure short month names do not cause false positives at the end of a word - mar (march)
        self.assertExpectedResult(self.cal.parse('lamar', start), (start, 0))
        # ensure short weekday names do not cause false positives within a word - mon (monday)
        self.assertExpectedResult(self.cal.parse('demonize', start), (start, 0))
        # ensure short weekday names do not cause false positives at the start of a word - mon (monday)
        self.assertExpectedResult(self.cal.parse('money', start), (start, 0))
        # ensure short weekday names do not cause false positives at the end of a word - th (thursday)
        self.assertExpectedResult(self.cal.parse('month', start), (start, 0))
        self.assertExpectedErrorFlag(self.cal.parse('30/030/01/071/07', start), (start, 0))


if __name__ == "__main__":
    unittest.main()
