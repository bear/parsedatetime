# -*- coding: utf-8 -*-
"""
Provides support for loading test data from files and preparing it for
convenient testing.

The primary interface used for testing is the `pdtFixture` function.
"""
from __future__ import unicode_literals

from datetime import datetime, timedelta
import glob
import inspect
import os
import pytest

from parsedatetime import Calendar, Constants, VERSION_CONTEXT_STYLE
from parsedatetime.context import pdtContext
from tests.data import datedelta, loadData, nlpTarget
from tests import log

INC_KEYS = ('months', 'years')
TIMEDELTA_KEYS = ('days', 'weeks', 'hours', 'minutes', 'seconds',
                  'milliseconds', 'microseconds')

KNOWN_PARAMETERS = ('sourceTime', 'target', 'nlpTarget', 'phrase', 'cal',
                    'context')
"""Tuple[str]: The parameter names for which `pdtFixture` can provide test
data (via `parameterValues`)."""

basedir = os.path.dirname(__file__)


def pdtFixture(filename, explicitTestGroupNames=None, localeIDs=None):
    """A decorator for test functions that uses data from the specified file
    to parametrize the test.

    The `pdtFixture` decorator supports the following arguments based on the
    test data:

    cal
        A `Calendar` preconfigured according to the test data and locale.
    phrase
        The string to be tested.
    sourceTime
        The `datetime.datetime` that the test data expects to be provided when
        processing the phrase. If not provided, `datetime.datetime.now()` will
        be used as the ``sourceTime``.
    target
        The target value specified in the test, usually a `datetime.datetime`.
        When test data targets a date or time delta, ``target`` will be
        resolved to a `datetime.datetime` relative to `sourceTime`. The
        ``target`` cannot be omitted; tests intentionally targeting invalid
        cases must explicitly specify ``target: null``.
    context
        The `pdtContext` that should represent the date and time components
        within the phrase.

    Examples:
        Tests are automatically parametrized across all locales with data from
        the test group matching the test name in the specified data file::

            @pdtFixture('deltas.yml')
            def test_past_float_deltas(cal, phrase, sourceTime, target, context):
                assert cal.parse(phrase, sourceTime) == (target, context)

        This will load the *past_float_deltas* test group from ``deltas.yml``
        then parametrize the function with `@pytest.mark.parametrize` for all
        phrases in all cases in the test group. All locales that include a
        ``deltas.yml`` with a *past_float_deltas* test group will be included
        in this test.

        If all phrases pass for this test case, the test results will include a
        pass count of 1. However, for each phrase that fails the failure count
        will be incremented by 1. Since parametrization allows each python test
        function to run against many different combinations of parameters it is
        important to understand that a single python test function may emit
        multiple failures.

        Tests may span multiple test groups::

            @pdtFixture('deltas.yml', ['past_int_deltas', 'past_float_deltas'])
            def test_deltas_wrapped_in_quotes(cal, phrase, sourceTime, target, context):
                assert cal.parse(u'"%s"' % phrase, sourceTime) == (target, context)

        While generally discouraged, in some cases it may be necessary to
        restrict tests to specific locales::

            @pdtFixture('deltas.yml', ['simple_multiple_unit_deltas'], ['en_US', 'en_AU'])
            def test_multiunit_deltas_with_from_today_suffix(cal, phrase, sourceTime, target, context):
                assert cal.parse(u'%s from today' % phrase, sourceTime) == (target, context)

        It is also possible to combine `pdtContext` with
        ``@pytest.mark.parametrize`` for additional test combinations::

            @pdtFixture('deltas.yml')
            @pytest.mark.parametrize('prefix,suffix', [('"','"'), ('(',')'), ('[',']')])
            def test_past_float_deltas(cal, phrase, sourceTime, target, context, prefix, suffix):
                assert cal.parse(u'%s%s%s' % (prefix, phrase, suffix), sourceTime) == (target, context)

        In this test, every phrase from `pdtContext` will be tested against
        every combination of parameters in ``@pytest.mark.parametrize``.

    Args:
        filename (str): The name of the file from which to load test data
            relative to the locale directory in the test fixtures. The file
            will be loaded from :file:`./tests/fixtures/{localeID}/{filename}`
            and must include the proper extension.
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
        testGroupNames = explicitTestGroupNames or \
            [testFn.__name__.replace('test_', '')]
        parameterization = generateParameters(filename, testGroupNames,
                                              parameters, localeIDs)

        return pytest.mark.parametrize(*parameterization)(testFn)
    return decorator


def generateParameters(filename, testGroupNames, parameters, localeIDs=None):
    """Collects all parameters from all test groups and returns a tuple that
    can be passed as ``*args`` to `@pytest.mark.parametrize`.

    Args:
        filename (str): The name of the test data file, including the ``.yml``
            extension.
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
    paths = glob.iglob(os.path.join(basedir, 'fixtures', localeID, filename))
    knownParameters = [param for param in parameters
                       if param in KNOWN_PARAMETERS]
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
            parameterGroups += parameterValues(group, knownParameters,
                                               localeID)

    return (','.join(knownParameters), parameterGroups)


def parameterValues(group, parameters, localeID):
    """Prepares fixture values required by the named parameters.

    Adding support for a new parameter value requires addition of the
    parameter name to `KNOWN_PARAMETERS`.

    Args:
        group (Dict[str, Dict]): The test group exactly as specified in the
            test data file
        parameters (List[str]): The parameters for which values should be
            prepared
        localeID (str): The locale identifier from which the test group was
            loaded, for the purpose of constructing the correct `Calendar`

    Returns:
        List[List]: The values corresponding to each parameter for each test
        case.
    """
    values = []
    constants = Constants(localeID, usePyICU=False)
    cal = Calendar(constants, version=VERSION_CONTEXT_STYLE)

    for case in normalizedCases(group, cal):
        for phrase, target in case['phrases']:
            caseValues = []
            context = case.get('context') or \
                pdtContext(pdtContext.ACU_WILDCARD)
            for parameter in parameters:
                if parameter == 'sourceTime':
                    caseValues.append(case['sourceTime'])
                elif parameter == 'target':
                    caseValues.append(target)
                elif parameter == 'phrase':
                    caseValues.append(phrase)
                elif parameter == 'context':
                    caseValues.append(context)
                elif parameter == 'cal':
                    caseValues.append(cal)
                elif parameter == 'nlpTarget':
                    caseValues.append(targetForNLP(target, phrase, context))
            values.append(caseValues)
    return values


def normalizedCases(group, calendar):
    """Pulls inherited data from the test group down to each case as required.

    Case markup is flexible to avoid excessive repetition between cases in a
    group. However, to ease parametrization each test case will be returned
    with a complete set of attributes.

    Args:
        group (Dict[str, Dict]): The test group data exactly as specified in
            the test data file
        calendar (Calendar): The `Calendar` for the current locale

    Returns:
        List[Dict[str, Any]]: A complete set of the following attributes for
        each test case:

        sourceTime
            The time relative to which the phrase will be evaluated.
        context
            The expected `pdtContext` for all phrases.
        phrases
            A list of ``(phrase, target)`` tuples with targets provided by
            `normalizeTarget`.
    """
    sourceTime = group.get('sourceTime') or datetime.now()
    context = group.get('context')
    cases = []

    for case in group['cases']:
        normCase = {
            'sourceTime': case.get('sourceTime') or sourceTime,
            'context': case.get('context') or context
        }
        phrases = case['phrases']

        if isinstance(phrases, dict):
            phrases = phrases.items()

        normCase['phrases'] = [(phrase, normalizedTarget(case['target'],
                                                         sourceTime, calendar,
                                                         phrase))
                               for phrase in phrases]

        cases.append(normCase)

    return cases


def normalizedTarget(target, sourceTime, calendar, phrase=None):
    """Coerces date deltas to `datetime`; other targets are passed through
    as-is.

    Args:
        target (Any): Any value; objects returned by `datedeltaConstructor`
            will be converted to `datetime.datetime` via `Calendar.inc` and
            `datetime.timedelta`.
        sourceTime (datetime.datetime): The datetime relative to which the test
            will be run.
        calendar (Calendar): A calendar corresponding to the locale from which
            the data was loaded.
        phrase (Optional[str]): The phrase associated with this target, for
            calculating indexes in `nlpTarget`.

    Returns:
        Any: While generally a `datetime.datetime`, this may be any value
        targeted by the test data
    """
    if isinstance(target, datedelta):
        target.calendar = calendar
        # Respect the sourceTime set on the datedelta
        if target.sourceTime:
            return target.sourceTime + target
        return sourceTime + target
    if isinstance(target, nlpTarget):
        target.calendar = calendar
        target.sourceTime = sourceTime
        target.sourcePhrase = phrase
    return target


def targetForNLP(target, phrase, context):
    """Constructs a tuple for comparison against the return value of
    `Calendar.nlp`.



    Args:
        target (Union[datetime.datetime,nlpTarget]): Description
        phrase (str): The complete string in which the `target` is found.
        context (pdtContext): The context corresponding either to the phrase in
            the `nlpTarget` if provided, or to the `phrase` argument.

    Returns:
        Tuple[Tuple[datetime,pdtContext,int,int,str]]: A tuple matching the
        return value of `nlp`.
    """
    if isinstance(target, nlpTarget):
        return target
    else:
        return ((target, context, 0, len(phrase), phrase),)
