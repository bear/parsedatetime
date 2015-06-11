
"""
Test parsing of 'simple' offsets
"""

import time
import datetime
import calendar
import unittest
import parsedatetime as pdt

def _truncateResult(result, trunc_seconds=True, trunc_hours=False):
    try:
        dt, flag = result
    except ValueError:
        # wtf?!
        return result
    if trunc_seconds:
        dt = dt[:5] + (0,) * 4
    if trunc_hours:
        dt = dt[:3] + (0,) * 6
    return dt, flag

_tr = _truncateResult

class test(unittest.TestCase):

    @pdt.tests.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return pdt.tests.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        self.cal = pdt.Calendar()
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testNow(self):
        s = datetime.datetime.now()

        start = s.timetuple()
        target = s.timetuple()

        self.assertExpectedResult(self.cal.parse('now', start), (target, 2))

    def testMinutesFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('5 minutes from now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 min from now',     start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5m from now',        start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in 5 minutes',       start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in 5 min',           start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 minutes',          start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 min',              start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5m',                 start), (target, 2))

        self.assertExpectedResult(self.cal.parse('five minutes from now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five min from now',     start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in five minutes',       start), (target, 2))
        self.assertExpectedResult(self.cal.parse('in five min',           start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five minutes',          start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five min',              start), (target, 2))

    def testMinutesBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(minutes=-5)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('5 minutes before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 min before now',     start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5m before now',        start), (target, 2))
        self.assertExpectedResult(self.cal.parse('5 minutes ago',        start), (target, 2))

        self.assertExpectedResult(self.cal.parse('five minutes before now', start), (target, 2))
        self.assertExpectedResult(self.cal.parse('five min before now',     start), (target, 2))

    def testWeekFromNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('in 1 week',           start), (target, 1))
        self.assertExpectedResult(self.cal.parse('1 week from now',     start), (target, 3))
        self.assertExpectedResult(self.cal.parse('in one week',         start), (target, 1))
        self.assertExpectedResult(self.cal.parse('one week from now',   start), (target, 3))
        self.assertExpectedResult(self.cal.parse('in a week',           start), (target, 1))
        self.assertExpectedResult(self.cal.parse('a week from now',     start), (target, 3))
        self.assertExpectedResult(self.cal.parse('in 7 days',           start), (target, 1))
        self.assertExpectedResult(self.cal.parse('7 days from now',     start), (target, 3))
        self.assertExpectedResult(self.cal.parse('in seven days',       start), (target, 1))
        self.assertExpectedResult(self.cal.parse('seven days from now', start), (target, 3))
        self.assertEqual(_tr(self.cal.parse('next week', start),
                             trunc_hours=True),
                         _tr((target, 1), trunc_hours=True))

    def testNextWeekDay(self):
        start = datetime.datetime.now()
        target = start + datetime.timedelta(days=4 + 7 - start.weekday())
        start = start.timetuple()
        target = target.timetuple()

        self.assertExpectedResult(self.cal.parse('next friday', start),
                                        (target, 1), dateOnly=True)
        self.assertExpectedResult(self.cal.parse('next friday?', start),
                                        (target, 1), dateOnly=True)
        self.cal.ptc.StartTimeFromSourceTime = True
        self.assertExpectedResult(self.cal.parse('next friday', start),
                                        (target, 1))

    def testWeekBeforeNow(self):
        s = datetime.datetime.now()
        t = s + datetime.timedelta(weeks=-1)

        start = s.timetuple()
        target = t.timetuple()

        self.assertEqual(_tr(self.cal.parse('1 week before now', start)),
                         _tr((target, 3)))
        self.assertEqual(_tr(self.cal.parse('one week before now', start)),
                         _tr((target, 3)))
        self.assertEqual(_tr(self.cal.parse('a week before now', start)),
                         _tr((target, 3)))
        self.assertEqual(_tr(self.cal.parse('7 days before now', start)),
                         _tr((target, 3)))
        self.assertEqual(_tr(self.cal.parse('seven days before now', start)),
                         _tr((target, 3)))
        self.assertEqual(_tr(self.cal.parse('1 week ago', start)),
                         _tr((target, 1)))
        self.assertEqual(_tr(self.cal.parse('a week ago', start)),
                         _tr((target, 1)))
        self.assertEqual(_tr(self.cal.parse('last week', start), trunc_hours=True),
                         _tr((target, 1), trunc_hours=True))

    def testNextMonth(self):
        s = datetime.datetime(self.yr, self.mth, self.dy, self.hr, self.mn, self.sec) + datetime.timedelta(days=1)
        t = self.cal.inc(s, year=1)

        start = s.timetuple()
        target = t.timetuple()

        phrase = 'next %s %s' % (calendar.month_name[t.month], t.day)

        self.assertEqual(_tr(self.cal.parse(phrase, start)), 
                         _tr((target, 1)))

    def testSpecials(self):
        s = datetime.datetime.now()
        t = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('tomorrow', start), (target, 1))
        self.assertExpectedResult(self.cal.parse('next day', start), (target, 1))

        t      = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0) + datetime.timedelta(days=-1)
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('yesterday', start), (target, 1))

        t      = datetime.datetime(self.yr, self.mth, self.dy, 9, 0, 0)
        target = t.timetuple()

        self.assertExpectedResult(self.cal.parse('today', start), (target, 1))


if __name__ == "__main__":
    unittest.main()
