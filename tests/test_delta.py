from .fixtures import pdtFixture


@pdtFixture('deltas.yml')
def test_past_integer_values(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_past_float_values(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_simple_multiple_unit_deltas(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_abbreviated_multiple_unit_deltas(calendar, phrase, sourceTime, target,
                                          context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)
