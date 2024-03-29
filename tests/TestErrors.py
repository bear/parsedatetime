# -*- coding: utf-8 -*-
"""
Test parsing of units
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

    @utils.assertEqualWithComparator
    def assertExpectedErrorFlag(self, result, check, **kwargs):
        return utils.compareResultByFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testErrors(self):
        s = datetime.datetime.now()
        start = s.timetuple()

        # These tests all return current date/time as they are out of range
        self.assertExpectedResult(self.cal.parse('01/0', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('08/35', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('18/35', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('1799', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('781', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('2702', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('78', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('11', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('1', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('174565', start), (start, pdtContext()))
        self.assertExpectedResult(self.cal.parse('177505', start), (start, pdtContext()))
        # ensure short month names do not cause false positives within a word -
        # jun (june)
        self.assertExpectedResult(
            self.cal.parse('injunction', start), (start, pdtContext()))
        # ensure short month names do not cause false positives at the start of
        # a word - jul (juuly)
        self.assertExpectedResult(self.cal.parse('julius', start), (start, pdtContext()))
        # ensure short month names do not cause false positives at the end of a
        # word - mar (march)
        self.assertExpectedResult(self.cal.parse('lamar', start), (start, pdtContext()))
        # ensure short weekday names do not cause false positives within a word
        # - mon (monday)
        self.assertExpectedResult(
            self.cal.parse('demonize', start), (start, pdtContext()))
        # ensure short weekday names do not cause false positives at the start
        # of a word - mon (monday)
        self.assertExpectedResult(self.cal.parse('money', start), (start, pdtContext()))
        # ensure short weekday names do not cause false positives at the end of
        # a word - th (thursday)
        self.assertExpectedResult(self.cal.parse('month', start), (start, pdtContext()))
        self.assertExpectedErrorFlag(
            self.cal.parse('30/030/01/071/07', start), (start, pdtContext()))
        # overflow due to Python's datetime
        self.assertExpectedResult(self.cal.parse('12345 y', start), (start, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('654321 w', start), (start, pdtContext()))
        self.assertExpectedResult(
            self.cal.parse('3700000 d', start), (start, pdtContext()))


if __name__ == "__main__":
    unittest.main()
