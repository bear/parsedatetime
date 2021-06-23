# -*- coding: utf-8 -*-
"""
Test time delta
"""

import sys
import time
import datetime
import parsedatetime as pdt

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


# added to support Python 2.6 which does not have total_seconds() method for timedelta
def total_seconds(timedelta):
    return (timedelta.microseconds + 0.0 +
            (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6


class test(unittest.TestCase):

    def setUp(self):
        self.cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
        self.source = (2017, 1, 1, 7, 1, 2, 6, 1, 1)

    def assertDelta(self, ts, years=None, months=None, **deltakw):
        ts = ts[0]
        source = self.source
        delta = datetime.timedelta(**deltakw)
        calc_delta = (datetime.datetime(*ts[:6]) -
                      datetime.datetime(*source[:6]))
        delta -= datetime.timedelta(microseconds=delta.microseconds)
        if not years and not months:
            self.assertEqual(delta, calc_delta)
            return
        if years:
            delta += datetime.timedelta(days=365 * years)
        if months:
            delta += datetime.timedelta(days=30 * months)
        diff = abs((total_seconds(calc_delta) -
                    total_seconds(delta)) /
                   total_seconds(delta))
        self.assertTrue(diff < 0.05, '%s is not less than 0.05' % diff)

    def testInteger(self):
        self.assertDelta(
            self.cal.parse('5 minutes ago', self.source), minutes=-5)
        self.assertDelta(
            self.cal.parse('34 hours ago', self.source), hours=-34)
        self.assertDelta(
            self.cal.parse('2 days ago', self.source), days=-2)

    def testFloat(self):
        self.assertDelta(
            self.cal.parse('58.4 minutes ago', self.source), minutes=-58.4)
        self.assertDelta(
            self.cal.parse('1855336.424 minutes ago', self.source),
            minutes=-1855336.424)
        self.assertDelta(
            self.cal.parse('8.3 hours ago', self.source), hours=-8.3)
        self.assertDelta(
            self.cal.parse('22.355 hours ago', self.source), hours=-22.355)
        self.assertDelta(
            self.cal.parse('7.2 days ago', self.source), days=-7.2)
        self.assertDelta(
            self.cal.parse('7.3 days ago', self.source), days=-7.3)
        self.assertDelta(
            self.cal.parse('17.7 days ago', self.source), days=-17.7)
        self.assertDelta(
            self.cal.parse('1.4 months ago', self.source), months=-1.4)
        self.assertDelta(
            self.cal.parse('4.8 months ago', self.source), months=-4.8)
        self.assertDelta(
            self.cal.parse('5.1 months ago', self.source), months=-5.1)
        self.assertDelta(
            self.cal.parse('5.11553 years ago', self.source), years=-5.11553)


if __name__ == "__main__":
    unittest.main()
