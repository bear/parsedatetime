import datetime
import string

from tests.lib.fixtures import pdtFixture


@pdtFixture('simple_datetimes.yml')
def test_times(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_invalid_times(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_dates(calendar, phrase, sourceTime, target, context,
               assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_invalid_dates(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_day_suffixes(calendar, phrase, sourceTime, target, context,
                      assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_special_times(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_midnight(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_noon(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_datetimes.yml')
def test_leap_days(calendar, phrase, sourceTime, target, context,
                   assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_year_parse_style_1(calendar, phrase, sourceTime, target, context,
                            assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('simple_datetimes.yml')
def test_year_parse_style_0(calendar, phrase, sourceTime, target, context,
                            assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


def test_days_in_month(calendar):
    dNormal = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    dLeap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    for i in range(1, 12):
        assert calendar.ptc.daysInMonth(i, 1999) == dNormal[i - 1]
        assert calendar.ptc.daysInMonth(i, 2000) == dLeap[i - 1]
        assert calendar.ptc.daysInMonth(i, 2001) == dNormal[i - 1]
        assert calendar.ptc.daysInMonth(i, 2002) == dNormal[i - 1]
        assert calendar.ptc.daysInMonth(i, 2003) == dNormal[i - 1]
        assert calendar.ptc.daysInMonth(i, 2004) == dLeap[i - 1]
        assert calendar.ptc.daysInMonth(i, 2005) == dNormal[i - 1]


def test_word_boundaries(calendar):
    start = target = datetime.datetime.now().timetuple()
    loc = calendar.ptc.locale
    keywords = []

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
        assert calendar.parse(phrase, start) == (target, 0)
