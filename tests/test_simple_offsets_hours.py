from .fixtures import pdtFixture


@pdtFixture('simple_offsets_hours.yml')
def test_hours_from_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple_offsets_hours.yml')
def test_invalid_hours_from_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (sourceTime.timetuple(),
                                                  context)


@pdtFixture('simple_offsets_hours.yml')
def test_hours_before_now(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)
