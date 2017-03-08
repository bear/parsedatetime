# -*- coding: utf-8 -*-
"""
Provides support for loading test data from files and preparing it for
convenient testing.

The primary interface used for testing is the `pdtFixture` function.
"""
from __future__ import unicode_literals

import glob
import inspect
import os
import pytest

from parsedatetime import Calendar
from .data import loadData, TestGroup
from tests import log


@pytest.fixture
def calendar():
    """A pytest fixture that provides a calendar with the default configuration
    for use in tests that do not make use of `pdtFixture`.

    Returns:
        parsedatetime.Calendar: A calendar with the default configuration.
    """
    return Calendar()


def pdtFixture(filename, explicitTestGroupNames=None, localeIDs=None):
    """A decorator for test functions that uses data from the specified file
    to parametrize the test.

    The `pdtFixture` decorator supports the following arguments based on the
    test data:

    calendar
        A `Calendar` preconfigured according to the test data and locale.
    phrase
        The string to be tested.
    sourceTime
        One or more `datetime.datetime` values against which to run the test.
        If not provided, the test will be parametrized against several common
        edge case dates. A `dateReplace` can be used here to modify the default
        edge case dates, for example to ensure that the month is January so
        that dates in February are interpreted within the same year rather than
        the following year.
    target
        The target value specified in the test, usually a `datetime.datetime`
        or `nlpTarget`. When test data targets a `datedelta`, `timedelta`, or
        `dateReplace`, ``target`` will be resolved to a `datetime.datetime`
        relative to `sourceTime`. The ``target`` cannot be omitted; tests
        intentionally targeting invalid cases must explicitly specify ``target:
        null``.
    context
        The `pdtContext` that should represent the date and time components
        within the phrase.

    Examples:
        Tests are automatically parametrized across all locales with data from
        the test group matching the test name in the specified data file::

            @pdtFixture('deltas.yml')
            def test_past_float_deltas(calendar, phrase, sourceTime, target, context):
                assert cal.parse(phrase, sourceTime) == (target, context)

        This will load the *past_float_deltas* test group from ``deltas.yml``
        then parametrize the function with `@pytest.mark.parametrize` for all
        phrases in all cases in the test group. All locales that include a
        ``deltas.yml`` with a *past_float_deltas* test group will be included
        in this test.

        Since parametrization allows each python test function to run against
        many different combinations of parameters it is important to understand
        that a single python test function may emit multiple successes or
        failures.

        Tests may span multiple test groups::

            @pdtFixture('deltas.yml', ['past_int_deltas', 'past_float_deltas'])
            def test_deltas_wrapped_in_quotes(calendar, phrase, sourceTime, target, context):
                assert calendar.parse(u'"%s"' % phrase, sourceTime) == (target, context)

        While generally discouraged, in some cases it may be necessary to
        restrict tests to specific locales::

            @pdtFixture('deltas.yml', ['simple_multiple_unit_deltas'], ['en_US', 'en_AU'])
            def test_multiunit_deltas_with_from_today_suffix(calendar, phrase, sourceTime, target, context):
                assert calendar.parse(u'%s from today' % phrase, sourceTime) == (target, context)

        It is also possible to combine `pdtContext` with
        ``@pytest.mark.parametrize`` for additional test combinations::

            @pytest.mark.parametrize('prefix,suffix', [('"','"'), ('(',')'), ('[',']')])
            @pdtFixture('deltas.yml')
            def test_past_float_deltas(calendar, phrase, sourceTime, target, context, prefix, suffix):
                assert calendar.parse(u'%s%s%s' % (prefix, phrase, suffix), sourceTime) == (target, context)

        In this test, every phrase from `pdtContext` will be tested against
        every combination of parameters in ``@pytest.mark.parametrize``.

    Args:
        filename (str): The name of the file from which to load test data
            relative to the locale directory. The file will be loaded from
            :file:`./tests/data/{localeID}/{filename}` and must include the
            proper extension.
        explicitTestGroupNames (Optional[List[str]]): The specific test
            groups to load from the specified fixture data file. If
            unspecified, `pdtFixture` will look for a test group matching the
            python test function name. Wildcards are not supported to
            ensure consistent behavior.
        localeIDs (Optional[List[str]]): A list of locale
            identifiers supported by `pdt_locales`, or ``None`` to load
            corresponding test data from all locales. Defaults to ``None``.

    Returns:
        Callable[[Callable], Callable]: A decorator for parametrizing test
        functions.

        The decorator populates the parameters required by the test function
        according to the arguments provided to `pdtFixture` then passes them
        along to ``@pytest.mark.parametrize``. The test function will be run
        for each set of parameters. Additional test combinations can be
        achieved by marking the test case with ``@pytest.mark.parametrize``.
        For more detail, see `the pytest documentation on parametrization
        <@pytest.mark.parametrize>`.
    """
    def decorator(testFn):
        parameters = inspect.getargspec(testFn)[0]
        basedir = os.path.dirname(inspect.getsourcefile(testFn))
        testGroupNames = explicitTestGroupNames or \
            [testFn.__name__.replace('test_', '')]
        parameterization = generateParameters(filename, basedir, testGroupNames,
                                              parameters, localeIDs)

        return pytest.mark.parametrize(*parameterization)(testFn)
    return decorator


def generateParameters(filename, basedir, testGroupNames, parameters,
                       localeIDs=None):
    """Collects all parameters from all test groups and returns a tuple that
    can be passed as ``*args`` to `@pytest.mark.parametrize`.

    Args:
        filename (str): The name of the test data file, including the ``.yml``
            extension.
        basedir (str): The directory of the test file, relative to which the
            data will be loaded.
        testGroupNames (List[str]): The test groups from the specified file
            that should be included in the parametrization.
        parameters (List[str]): The parameter names required by the test
            function.
        localeIDs (Optional[List[str]]): A list of locale identifiers supported
            by `pdt_locales`, or ``None`` to load corresponding test data from
            all locales. Defaults to ``None``.

    Returns:
        Tuple[str, List[Tuple]: A tuple that can be passed as ``*args`` to
        `@pytest.mark.parametrize`.

        The first element in the tuple is a string representing the arguments
        that will be provided for the testing function. The order corresponds
        to the order of values in all of the tuples in the second element.
    """
    localeID = localeIDs[0] if localeIDs and len(localeIDs) == 1 else '*'
    paths = glob.iglob(os.path.join(basedir, 'data', localeID, filename))
    knownParameters = TestGroup.supportedParameters(parameters)
    parameterGroups = []

    for path in paths:
        localeID = os.path.basename(os.path.dirname(path))

        if localeIDs and localeID not in localeIDs:
            continue

        allGroups = loadData(path)

        if not allGroups:
            continue

        testGroups = [group for groupName, group in allGroups.items()
                      if groupName in testGroupNames]
        unsupportedTests = [groupName for groupName in testGroupNames
                            if groupName not in allGroups]

        # TODO: summary after tests of any unsupported cases
        for unsupportedTest in unsupportedTests:
            log.warn('Locale %s does not provide test %s', localeID,
                     unsupportedTest)

        for group in testGroups:
            group = TestGroup(group, localeID)
            parameterGroups += group.parameterValues(knownParameters)

    return (','.join(knownParameters), parameterGroups)
