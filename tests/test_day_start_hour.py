from .fixtures import pdtFixture


@pdtFixture('day_start_hour.yml')
def test_default_day_start_hour(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('day_start_hour.yml')
def test_midnight_day_start_hour(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('day_start_hour.yml')
def test_morning_day_start_hour(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('day_start_hour.yml')
def test_evening_day_start_hour(calendar, phrase, sourceTime, target, context):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)