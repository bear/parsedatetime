from .fixtures import pdtFixture


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
