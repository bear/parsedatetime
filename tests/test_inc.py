import datetime

from .fixtures import pdtFixture


def test_inc_months(calendar):
    s = datetime.datetime(2006, 1, 1, 12, 0, 0)
    t = datetime.datetime(2006, 2, 1, 12, 0, 0)
    assert calendar.inc(s, month=1).timetuple() == t.timetuple()

    s = datetime.datetime(2006, 12, 1, 12, 0, 0)
    t = datetime.datetime(2007, 1, 1, 12, 0, 0)
    assert calendar.inc(s, month=1).timetuple() == t.timetuple()

    # leap year, Feb 1
    s = datetime.datetime(2008, 2, 1, 12, 0, 0)
    t = datetime.datetime(2008, 3, 1, 12, 0, 0)
    assert calendar.inc(s, month=1).timetuple() == t.timetuple()

    # leap year, Feb 29
    s = datetime.datetime(2008, 2, 29, 12, 0, 0)
    t = datetime.datetime(2008, 3, 29, 12, 0, 0)
    assert calendar.inc(s, month=1).timetuple() == t.timetuple()

    s = datetime.datetime(2006, 1, 1, 12, 0, 0)
    t = datetime.datetime(2005, 12, 1, 12, 0, 0)
    assert calendar.inc(s, month=-1).timetuple() == t.timetuple()

    # End of month Jan 31 to Feb - Febuary only has 28 days
    s = datetime.datetime(2006, 1, 31, 12, 0, 0)
    t = datetime.datetime(2006, 2, 28, 12, 0, 0)
    assert calendar.inc(s, month=1).timetuple() == t.timetuple()

    # walk thru months and make sure month increment doesn't set the day
    # to be past the last day of the new month
    # think Jan transition to Feb - 31 days to 28 days
    for m in range(1, 11):
        d = calendar.ptc.daysInMonth(m, 2006)
        s = datetime.datetime(2006, m, d, 12, 0, 0)

        if d > calendar.ptc.daysInMonth(m + 1, 2006):
            d = calendar.ptc.daysInMonth(m + 1, 2006)

        t = datetime.datetime(2006, m + 1, d, 12, 0, 0)

        assert calendar.inc(s, month=1).timetuple() == t.timetuple()

def test_inc_years(calendar):
    s = datetime.datetime(2006, 1, 1, 12, 0, 0)
    t = datetime.datetime(2007, 1, 1, 12, 0, 0)
    assert calendar.inc(s, year=1).timetuple() == t.timetuple()

    s = datetime.datetime(2006, 1, 1, 12, 0, 0)
    t = datetime.datetime(2008, 1, 1, 12, 0, 0)
    assert calendar.inc(s, year=2).timetuple() == t.timetuple()

    s = datetime.datetime(2006, 12, 31, 12, 0, 0)
    t = datetime.datetime(2007, 12, 31, 12, 0, 0)
    assert calendar.inc(s, year=1).timetuple() == t.timetuple()

    s = datetime.datetime(2006, 12, 31, 12, 0, 0)
    t = datetime.datetime(2005, 12, 31, 12, 0, 0)
    assert calendar.inc(s, year=-1).timetuple() == t.timetuple()

    s = datetime.datetime(2008, 3, 1, 12, 0, 0)
    t = datetime.datetime(2009, 3, 1, 12, 0, 0)
    assert calendar.inc(s, year=1).timetuple() == t.timetuple()

    s = datetime.datetime(2008, 3, 1, 12, 0, 0)
    t = datetime.datetime(2007, 3, 1, 12, 0, 0)
    assert calendar.inc(s, year=-1).timetuple() == t.timetuple()