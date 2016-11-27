from .fixtures import pdtFixture


@pdtFixture('ranges.yml')
def test_times(calendar, phrase, sourceTime, target, context):
    (startTarget, endTarget) = target
    assert (calendar.evalRanges(phrase, sourceTime) ==
            (startTarget.timetuple(), endTarget.timetuple(), context))


@pdtFixture('ranges.yml')
def test_dates(calendar, phrase, sourceTime, target, context,
               assertLazyStructTimes):
    (startTarget, endTarget) = target
    (start, end, resultContext) = calendar.evalRanges(phrase, sourceTime)
    assertLazyStructTimes(start, startTarget.timetuple())
    assertLazyStructTimes(end, endTarget.timetuple())
    assert resultContext == context
