from tests.lib.fixtures import pdtFixture


@pdtFixture('names.yml')
def test_week_day_names(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('names.yml')
def test_invalid_week_day_names(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('names.yml')
def test_month_names(calendar, phrase, sourceTime, target, context,
                     assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('names.yml')
def test_invalid_month_names(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)
