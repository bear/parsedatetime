from .fixtures import pdtFixture


@pdtFixture('start_time_from_source_time.yml')
def test_end_of_phrases_enabled(calendar, phrase, sourceTime, target, context,
               assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('start_time_from_source_time.yml')
def test_end_of_phrases_disabled(calendar, phrase, sourceTime, target, context,
               assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context
