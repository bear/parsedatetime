# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times using the Spanish locale
"""
from __future__ import unicode_literals

import sys
import time
import datetime
import parsedatetime as pdt
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
        self.ptc = pdt.Constants('es', usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)

        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

        if self.ptc.localeID != 'es':
            raise unittest.SkipTest(
                'Locale not set to es - check if PyICU is installed')

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('23:00:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('23:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('2300', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('11:00:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1100', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('730', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('0730', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('1730', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('173000', start), (target, 2))

    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2006, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('25/08/2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25/8/06', start), (target, 1))

        if self.mth > 8 or (self.mth == 8 and self.dy > 25):
            target = datetime.datetime(
                self.yr + 1, 8, 25, self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(
                self.yr, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('25-8', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25-08', start), (target, 1))

        if self.mth > 6 or (self.mth == 6 and self.dy > 13):
            target = datetime.datetime(
                self.yr + 1, 6, 13, self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(
                self.yr, 6, 13, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('13 de junio', start), (target, 1))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 9, 0, 0) - datetime.timedelta(days=2)
        target = target.timetuple()
        self.assertExpectedResult(
            self.cal.parse('anteayer', start), (target, 1))

    def testRanges(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy,
            self.hr, self.mn, self.sec).timetuple()

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) + datetime.timedelta(days=4)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) + datetime.timedelta(days=5)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("después de 4 días", start), (targetStart, targetEnd, 1))'''
        '''self.assertExpectedResult(
            self.cal.evalRanges("despues de 4 días", start), (targetStart, targetEnd, 1))'''
        self.assertExpectedResult(
            self.cal.evalRanges("4 dias", start), (targetStart, targetEnd, 1))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) - datetime.timedelta(days=4)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) - datetime.timedelta(days=3)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("4 días tarde", start), (targetStart, targetEnd, 1))'''

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) + datetime.timedelta(days=5)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("los próximos 5 días", start), (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("por los proximos 5 dias", start), (targetStart, targetEnd, 1))'''

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) - datetime.timedelta(days=5)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec)
        targetEnd = targetEnd.timetuple()
        self.assertExpectedResult(
            self.cal.evalRanges("desde 5 dias", start),  (targetStart, targetEnd, 1))

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) - datetime.timedelta(days=1) \
                      + datetime.timedelta(hours=1)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("desde 23 horas ", start), (targetStart, targetEnd, 1))'''

        targetStart = datetime.datetime(
            self.yr + 1, 1, 1, 9, 0, 0)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr + 2, 1, 1, 9, 0, 0)
        targetEnd = targetEnd.timetuple()
        self.assertExpectedResult(
            self.cal.evalRanges("el próximo año", start),
            (targetStart, targetEnd, 1))

        targetStart = datetime.datetime(
            self.yr - 1, 1, 1, 9, 0, 0)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, 1, 1, 9, 0, 0)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("el año pasado", start),
            (targetStart, targetEnd, 1))'''

        targetStart = datetime.datetime(
            self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=4)
        targetStart = targetStart.timetuple()
        targetEnd = datetime.datetime(
            self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=5)
        targetEnd = targetEnd.timetuple()
        '''self.assertExpectedResult(
            self.cal.evalRanges("3 días a partir de mañana", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("4 días a partir de hoy", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("6 días a partir de anteayer", start),
            (targetStart, targetEnd, 1))'''
        self.assertExpectedResult(
            self.cal.evalRanges("3 dias a partir de mañana", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("4 dias a partir de hoy", start),
            (targetStart, targetEnd, 1))
        self.assertExpectedResult(
            self.cal.evalRanges("6 dias a partir de anteayer", start),
            (targetStart, targetEnd, 1))


if __name__ == "__main__":
    unittest.main()
