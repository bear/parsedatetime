from tests.lib.fixtures import pdtFixture


@pdtFixture('errors.yml')
def test_out_of_range(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('errors.yml')
def test_plain_numbers(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('errors.yml')
def test_substring_phrases(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('errors.yml')
def test_substring_dates(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('errors.yml')
def test_overflow(calendar, phrase, sourceTime, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)
