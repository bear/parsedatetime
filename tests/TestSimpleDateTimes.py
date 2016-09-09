# -*- coding: utf-8 -*-
"""
Test parsing of simple date and times
"""
from __future__ import unicode_literals

import sys
import time
import datetime
import string
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
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testDays(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(days=1)

        start = s.timetuple()
        target = t.timetuple()

        d = self.wd + 1

        if d > 6:
            d = 0

        day = self.cal.ptc.Weekdays[d]

        self.assertExpectedResult(self.cal.parse(day, start), (target, 1))

        t = s + datetime.timedelta(days=6)

        target = t.timetuple()

        d = self.wd - 1

        if d < 0:
            d = 6

        day = self.cal.ptc.Weekdays[d]

        self.assertExpectedResult(self.cal.parse(day, start), (target, 1))

    def testTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 23, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('11:00:00 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('2300', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('23:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11p', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00:00 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11p.m.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 p.m.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('"11 p.m."', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 11, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('11:00:00 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1100', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11a', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11am', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00:00 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11:00 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11a.m.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('11 a.m.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('(11 a.m.)', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 7, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('730', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('0730', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('0730am', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 30, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('1730', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('173000', start), (target, 2))

        # Should not parse as a time due to prefix
        self.assertExpectedResult(self.cal.parse('$300', start), (start, 0))
        self.assertExpectedResult(self.cal.parse('300ml', start), (start, 0))

        # Should not parse as a time due to false meridian
        self.assertExpectedResult(self.cal.parse('3 axmx', start), (start, 0))
        self.assertExpectedResult(self.cal.parse('3 pxmx', start), (start, 0))

    def testDates(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2006, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('08/25/2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('08.25.2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('2006/08/25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('2006/8/25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('2006-08-25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('8/25/06', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 25, 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 25, 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 25, 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 25 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 25 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 25 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25 August 2006', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('25 Aug 2006', start), (target, 1))

        if self.mth > 8 or (self.mth == 8 and self.dy > 25):
            target = datetime.datetime(
                self.yr + 1, 8, 25, self.hr, self.mn, self.sec).timetuple()
        else:
            target = datetime.datetime(
                self.yr, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('8/25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('8.25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('08/25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 25', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('"8.25"', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('(8.25)', start), (target, 1))

        # Should not parse as dates
        self.assertExpectedResult(self.cal.parse('$1.23', start), (start, 0))
        self.assertExpectedResult(self.cal.parse('$12.34', start), (start, 0))

        # added test to ensure 4-digit year is recognized in the absence of day
        target = datetime.datetime(
            2013, 8, 1, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('Aug. 2013', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug  2013', start), (target, 1))

    def testLeapDays(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2000, 2, 29, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('02/29/2000', start), (target, 1))

        target = datetime.datetime(
            2004, 2, 29, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('02/29/2004', start), (target, 1))

        target = datetime.datetime(
            2008, 2, 29, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('02/29/2008', start), (target, 1))

        target = datetime.datetime(
            2012, 2, 29, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('02/29/2012', start), (target, 1))

        dNormal = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        dLeap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

        for i in range(1, 12):
            self.assertTrue(self.cal.ptc.daysInMonth(i, 1999), dNormal[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2000), dLeap[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2001), dNormal[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2002), dNormal[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2003), dNormal[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2004), dLeap[i - 1])
            self.assertTrue(self.cal.ptc.daysInMonth(i, 2005), dNormal[i - 1])

    def testDaySuffixes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            2008, 8, 22, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('August 22nd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 22nd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 22nd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 22nd 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 22nd 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 22nd 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('22nd August 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('22nd Aug 2008', start), (target, 1))

        target = datetime.datetime(
            1949, 12, 31, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('December 31st, 1949', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Dec 31st, 1949', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('December 31st 1949', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Dec 31st 1949', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('31st December 1949', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('31st Dec 1949', start), (target, 1))

        target = datetime.datetime(
            2008, 8, 23, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('August 23rd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 23rd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 23rd, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 23rd 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 23rd 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 23rd 2008', start), (target, 1))

        target = datetime.datetime(
            2008, 8, 25, self.hr, self.mn, self.sec).timetuple()

        self.assertExpectedResult(
            self.cal.parse('August 25th, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 25th, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 25th, 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('August 25th 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug 25th 2008', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('Aug. 25th 2008', start), (target, 1))

    def testSpecialTimes(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 6, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('morning', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 8, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('breakfast', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 12, 0, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('lunch', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 13, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('afternoon', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 18, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('evening', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 19, 0, 0).timetuple()

        self.assertExpectedResult(self.cal.parse('dinner', start), (target, 2))

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 21, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('night', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('tonight', start), (target, 2))

    def testMidnight(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 0, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('midnight', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00:00 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12 AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12AM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12am', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12a', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('0000', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('00:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00:00 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12 A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12A.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12a.m.', start), (target, 2))

    def testNoon(self):
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(
            self.yr, self.mth, self.dy, 12, 0, 0).timetuple()

        self.assertExpectedResult(
            self.cal.parse('noon', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00:00 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12 PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12PM', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12pm', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12p', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('1200', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00:00 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12:00 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12 P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12P.M.', start), (target, 2))
        self.assertExpectedResult(
            self.cal.parse('12p.m.', start), (target, 2))

    def testDaysOfWeek(self):
        start = datetime.datetime(
            2014, 10, 25, self.hr, self.mn, self.sec).timetuple()

        target = datetime.datetime(
            2014, 10, 26, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('sunday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('sun', start), (target, 1))

        target = datetime.datetime(
            2014, 10, 27, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('Monday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('mon', start), (target, 1))

        target = datetime.datetime(
            2014, 10, 28, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('tuesday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('tues', start), (target, 1))

        target = datetime.datetime(
            2014, 10, 29, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('wednesday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('wed', start), (target, 1))

        target = datetime.datetime(
            2014, 10, 30, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('thursday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('thu', start), (target, 1))

        target = datetime.datetime(
            2014, 10, 31, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('friday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('fri', start), (target, 1))

        target = datetime.datetime(
            2014, 11, 1, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('saturday', start), (target, 1))
        self.assertExpectedResult(
            self.cal.parse('sat', start), (target, 1))

    def testWordBoundaries(self):
        # Ensure that keywords appearing at the start of a word are not parsed
        # as if they were standalone keywords. For example, "10 dogs" should
        # not be interpreted the same as "10 d"
        start = datetime.datetime(
            self.yr, self.mth, self.dy, self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime.now().timetuple()

        keywords = []
        loc = self.cal.ptc.locale

        def flattenWeekdays(wds):
            return sum([wd.split('|') for wd in wds], [])

        # Test all known keywords for the locale
        keywords.extend(loc.meridian)
        keywords.extend(flattenWeekdays(loc.Weekdays))
        keywords.extend(flattenWeekdays(loc.shortWeekdays))
        keywords.extend(loc.Months)
        keywords.extend(loc.shortMonths)
        keywords.extend(loc.numbers.keys())
        keywords.extend(loc.Modifiers.keys())
        keywords.extend(loc.dayOffsets.keys())
        keywords.extend(loc.re_sources.keys())
        keywords.extend(loc.small.keys())
        keywords.extend(loc.magnitude.keys())

        for units in loc.units.values():
            keywords.extend(units)

        # Finally, test all lowercase letters to be particularly thorough - it
        # would be very difficult to track down bugs due to single letters.
        keywords.extend(list(string.ascii_lowercase))

        for keyword in keywords:
            phrase = '1 %sfoo' % keyword
            self.assertExpectedResult(
                self.cal.parse(phrase, start), (target, 0),
                'Result does not match target value: %s' % repr(phrase))

    def testYearParseStyle(self):
        config = pdt.Constants()
        config.YearParseStyle = 0
        calendar = pdt.Calendar(config)
        start = datetime.datetime(self.yr, self.mth, self.dy,
                                  self.hr, self.mn, self.sec).timetuple()
        target = datetime.datetime(self.yr, 7, 28,
                                   self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(calendar.parse('7/28', start), (target, 1))

    # def testMonths(self):

    #     start = datetime.datetime(
    #         self.yr, self.mth, self.dy,
    #         self.hr, self.mn, self.sec).timetuple()

    #     target = datetime.datetime(
    #         self.yr, self.mth, self.dy, 12, 0, 0).timetuple()

    #     self.assertExpectedResult(self.cal.parse('jun', start), (target, 2))
    #     self.assertExpectedResult(
    #         self.cal.parse('12:00:00 PM', start), (target, 2))
    #     self.assertExpectedResult(
    #         self.cal.parse('12:00 PM', start), (target, 2))
    #     self.assertExpectedResult(self.cal.parse('12 PM', start),
    #                               (target, 2))
    #     self.assertExpectedResult(self.cal.parse('12PM', start), (target, 2))
    #     self.assertExpectedResult(self.cal.parse('12pm', start), (target, 2))
    #     self.assertExpectedResult(self.cal.parse('12p', start), (target, 2))
    #     self.assertExpectedResult(self.cal.parse('1200', start), (target, 2))
    #     self.assertExpectedResult(self.cal.parse('12:00', start),
    #                               (target, 2))

if __name__ == "__main__":
    unittest.main()
