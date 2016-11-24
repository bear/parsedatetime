from .fixtures import pdtFixture


@pdtFixture('phrases.yml')
def test_phrases(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('phrases.yml')
def test_weekday_phrases(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('phrases.yml')
def test_end_of_phrases(calendar, phrase, sourceTime, target, context,
                        assertLazyStructTimes):
    result = calendar.parse(phrase, sourceTime)
    assertLazyStructTimes(result[0], target.timetuple())
    assert result[1] == context


@pdtFixture('phrases.yml')
def test_last_phrases(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)
