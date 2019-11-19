from tests.lib.fixtures import pdtFixture


@pdtFixture('targets.yml')
def test_target_by_phrase(calendar, phrase, sourceTime, target, context,
                          assertLazyStructTimes):
    assert calendar.parse(phrase, sourceTime) == (target.timetuple(), context)


@pdtFixture('simple.yml', explicitTestGroupNames=['noon'])
def test_unknown_parameters(phrase, target, case):
    assert case.parameterValues(['unknown']) == ((),)


@pdtFixture('simple.yml', explicitTestGroupNames=['noon'])
def test_single_parameter(phrase):
    assert phrase == 'noon'