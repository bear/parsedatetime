from .fixtures import pdtFixture


@pdtFixture('simple_datetimes.yml')
def test_times(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_invalid_times(cal, phrase, sourceTime, context):
    assert cal.parse(phrase, sourceTime) == (sourceTime.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_dates(cal, phrase, sourceTime, target, context,
               assertLazyStructTimes):
    result = cal.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_invalid_dates(cal, phrase, sourceTime, context):
    assert cal.parse(phrase, sourceTime) == (sourceTime.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_day_suffixes(cal, phrase, sourceTime, target, context,
                      assertLazyStructTimes):
    result = cal.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_special_times(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)

#
# Leap years
#


@pdtFixture('simple_datetimes.yml')
def test_leap_days(cal, phrase, sourceTime, target, context,
                   assertLazyStructTimes):
    result = cal.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


def test_days_in_month(cal):
    dNormal = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    dLeap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    for i in range(1, 12):
        assert cal.ptc.daysInMonth(i, 1999) == dNormal[i - 1]
        assert cal.ptc.daysInMonth(i, 2000) == dLeap[i - 1]
        assert cal.ptc.daysInMonth(i, 2001) == dNormal[i - 1]
        assert cal.ptc.daysInMonth(i, 2002) == dNormal[i - 1]
        assert cal.ptc.daysInMonth(i, 2003) == dNormal[i - 1]
        assert cal.ptc.daysInMonth(i, 2004) == dLeap[i - 1]
        assert cal.ptc.daysInMonth(i, 2005) == dNormal[i - 1]
