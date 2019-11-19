from tests.lib.fixtures import pdtFixture


@pdtFixture('complex_datetimes.yml')
def test_year_month_day_and_time(calendar, phrase, sourceTime, target,
                                 context, assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_future_month_day_and_time(calendar, phrase, sourceTime, target,
                                   context, assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_past_month_day_and_time(calendar, phrase, sourceTime, target,
                                 context, assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_date_variations(calendar, phrase, sourceTime, target, context,
                         assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_future_date_variations(calendar, phrase, sourceTime, target, context,
                                assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_past_date_variations(calendar, phrase, sourceTime, target, context,
                              assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('complex_datetimes.yml')
def test_dates_with_weekday(calendar, phrase, sourceTime, target, context,
                            assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context
