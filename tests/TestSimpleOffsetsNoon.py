# -*- coding: utf-8 -*-
"""
Test parsing of 'simple' offsets
"""
from __future__ import unicode_literals

import time
import datetime
import unittest
import parsedatetime as pdt
from . import utils


class test(unittest.TestCase):

    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return utils.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testOffsetAfterNoon(self):
        s = datetime.datetime(self.yr, self.mth, self.dy, 10, 0, 0)
        t = datetime.datetime(
            self.yr, self.mth, self.dy, 12, 0, 0) + datetime.timedelta(hours=5)

        start = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(
            self.cal.parse('5 hours after 12pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('five hours after 12pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours after 12 pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours after 12:00pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours after 12:00 pm', start), (target, 2))
        # self.assertExpectedResult(
        #     self.cal.parse('5 hours after noon', start), (target, 2))
        # self.assertExpectedResult(
        #     self.cal.parse('5 hours from noon', start), (target, 2))

    def testOffsetBeforeNoon(self):
        s = datetime.datetime.now()
        t = (datetime.datetime(self.yr, self.mth, self.dy, 12, 0, 0) +
             datetime.timedelta(hours=-5))

        start = s.timetuple()
        target = t.timetuple()

        # self.assertExpectedResult(
        #     self.cal.parse('5 hours before noon', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours before 12pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('five hours before 12pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours before 12 pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours before 12:00pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('5 hours before 12:00 pm', start), (target, 2))


if __name__ == "__main__":
    unittest.main()
