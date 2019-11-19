from tests.lib.fixtures import pdtFixture


@pdtFixture('simple_offsets.yml')
def test_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_offset_from_day_of_week(calendar, phrase, sourceTime, target,
                                 context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_offset_from_day_of_week_matching_source_time(calendar, phrase,
                                                      sourceTime, target,
                                                      context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_minutes_from_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_minutes_before_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_week_from_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_week_before_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_next_month(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_next_weekday(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_next_weekday_matching_source_time(calendar, phrase, sourceTime,
                                           target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_next_weekday_with_time(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets.yml')
def test_specials(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)
