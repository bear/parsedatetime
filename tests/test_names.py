from .fixtures import pdtFixture


@pdtFixture('names.yml')
def test_week_day_names(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('names.yml')
def test_invalid_week_day_names(cal, phrase, sourceTime, context):
    assert cal.parse(phrase, sourceTime) == (sourceTime.timetuple(), context)


@pdtFixture('names.yml')
def test_month_names(cal, phrase, sourceTime, target, context,
                     assertLazyStructTimes):
    result = cal.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context
