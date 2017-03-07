# -*- coding: utf-8 -*-
"""
Provides fixtures for custom assertions.

In some cases the data returned by parsedatetime is not strictly equivalent;
these assertions provide some flexibility for assertions.
"""
from __future__ import unicode_literals

import pytest
import time


@pytest.fixture
def assertLazyStructTimes():
    """A test fixture that compares `time.struct_time` values for cases where
    parsedatetime does not properly update a few flags.

    The fixture provides a function that can be called to compare two
    `time.struct_time` values, ignoring the ``wday``, ``yday``, and ``isdst``
    named fields.

    Example:
        The fixture is loaded by requesting it as an argument of the test
        function. Note that the function must be called with `time.struct_time`
        values and will not unwrap tuples such as those returned by
        `Calendar.parse` to find them::

            @pdtFixture('names.yml')
            def test_month_names(cal, phrase, sourceTime, target, context, assertLazyStructTimes):
                result = cal.parse(phrase, sourceTime)
                assertLazyStructTimes(result[0], target.timetuple())
                assert result[1] == context

    Returns:
        Callable[[time.struct_time, time.struct_time], None]: A function that
        can be used to compare two `time.struct_time` values.

    Raises:
        AssertionError: if the `time.struct_time` values are not equivalent
            after ignoring the specified fields.
    """
    def doAssertLazyStructTimes(a, b):
        assert ignoreWeekdayYeardayDST(a) == ignoreWeekdayYeardayDST(b)
    return doAssertLazyStructTimes


def ignoreWeekdayYeardayDST(st):
    return time.struct_time(st[:6] + (-1, -1, -1))
