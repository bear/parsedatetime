from .fixtures import pdtFixture


@pdtFixture('deltas.yml')
def test_past_integer_values(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_past_float_values(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_simple_multiple_unit_deltas(cal, phrase, sourceTime, target, context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('deltas.yml')
def test_abbreviated_multiple_unit_deltas(cal, phrase, sourceTime, target,
                                          context):
    assert cal.parse(phrase, sourceTime) == (target.timetuple(), context)
