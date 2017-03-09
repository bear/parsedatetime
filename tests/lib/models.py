# -*- coding: utf-8 -*-
"""
Convenience classes and 

In addition to the syntax supported by ``PyYaml``, parsedatetime provides a few
constructors to represent data in YAML.
"""

from datetime import datetime, timedelta
import re

from parsedatetime import Calendar, Constants, VERSION_CONTEXT_STYLE
from parsedatetime.context import pdtContext


# Allow Python 2 type checking in Python 3
try:
    unicode = unicode
except NameError:      # pragma: no cover
    basestring = (str, bytes)
    long = int


DEFAULT_SOURCE_TIMES = (
    datetime(2016, 2, 29, 3, 4, 5),
    datetime(2015, 2, 28, 23, 22, 21),
    datetime(1945, 12, 31, 3, 4, 5),
)

_PROPERTY_MAPPING = {
    'sourceTime': lambda case, target, phrase: case.sourceTime,
    'target': lambda case, target, phrase: case.resolveTarget(target, phrase),
    'phrase': lambda case, target, phrase: phrase,
    'context': lambda case, target, phrase: case.context,
    'calendar': lambda case, target, phrase: case.calendar,
    'nlpTarget': lambda case, target, phrase: case.nlpTarget(target, phrase),
    'case': lambda case, target, phrase: case,
}


class datedelta(object):
    """Represents a change in time over a number of years, months, or any unit
    supported by `datetime.timedelta`.

    Months are added or subtracted maintaining the date within the month. If
    the date is greater than the number of days in the month (e.g. moving from
    January 31 to February) the date is adjusted to the last day of the target
    month.

    Similarly, when a change in year produces an invalid date (e.g. Feb 29,
    2016 to 2017) the date is adjusted to the last day of the month.

    Months and years are added *before* the ``timedelta`` is applied. For
    example, adding 1 month to January 30 yields February 28 then adding one
    day yields March 1. If the ``timedelta`` were applied first, 1 day would be
    added to January 30 yielding January 31, then one month would be added
    yielding February 28.
    """

    def __init__(self, years=0, months=0, sourceTime=None, **kwargs):
        """Initialize a `datedelta`

        Args:
            years (Optional[int]): Number of years.
            months (Optional[int]): Number of months.
            sourceTime (Optional[Union[datetime.datetime, dateReplacement]]):
                The date relative to which this `datedelta` should be
                interpreted.
            calendar (Optional[parsedatetime.Calendar]): The calendar on which
                `Calendar.inc` will be called to handle year and month
                calculation.
            **kwargs: Keyed arguments acceptable to `datetime.timedelta`.

        Raises:
            TypeError: If any arguments are of the wrong type or if the
                ``**kwargs`` contain keys not supported by
                `datetime.timedelta`.
        """
        delta = timedelta(**kwargs)
        typeErrorMsg = 'unsupported type for datedelta %s component: %s'

        if not isinstance(years, (int, long)):
            raise TypeError(typeErrorMsg % ('years', type(years).__name__))
        if not isinstance(months, (int, long)):
            raise TypeError(typeErrorMsg % ('months', type(months).__name__))
        if not isinstance(sourceTime, (datetime, dateReplacement, type(None))):
            raise TypeError('unsupported type for datedelta %s: %s' %
                            ('sourceTime', type(sourceTime).__name__))

        self._years = years
        self._months = months
        self._sourceTime = sourceTime
        self._kwargs = kwargs
        self._timedelta = delta

    @property
    def years(self):
        """int: Number of years to offset a date."""
        return self._years

    @property
    def months(self):
        """int: Number of months to offset a date."""
        return self._months

    @property
    def sourceTime(self):
        """Union[datetime.datetime,dateReplacement]: The date relative to which
        this `datedelta` should always be interpreted. It is expected that any
        logic operating on a `datedelta` will check whether the `datedelta` has
        a `sourceTime` and if so, calculate a final date based on that rather
        than some other time.
        """
        return self._sourceTime

    def add(self, other, calendar):
        """Add the datedelta to the specified date.

        Args:
            other (datetime.datetime): The ``datetime`` to which the interval
                represented by this ``datedelta`` should be added.
            calendar (Calendar): The calendar responsible for year and month
                addition.

        Returns:
            datetime.datetime: The date adjusted according to the ``datedelta``
        """
        if isinstance(other, datetime):
            return (calendar.inc(other, self._months, self._years) +
                    self._timedelta)
        raise NotImplementedError

    def __repr__(self):
        return "%s(%d, %d, %s)" % (self.__class__.__name__,
                                   self._years,
                                   self._months,
                                   repr(self._timedelta))

    def __str__(self):
        def plural(n):
            return n, abs(n) != 1 and "s" or ""
        s = []
        if self._years:
            s.append('%d year%s' % plural(self._years))
        if self._months:
            s.append('%d month%s' % plural(self._months))
            
        s.append(str(self._timedelta))
        return ', '.join(s)


class dateReplacement(object):
    """A wrapper for `datetime.datetime.replace` allowing arbitrary
    modifications to individual fields in a `datetime.datetime`.
    """
    def __init__(self, **kwargs):
        """Initializes a `dateReplacement` with arguments suitable for
        `datetime.datetime.replace`.

        Args:
            **kwargs: Arguments for `datetime.datetime.replace`.

        Raises:
            TypeError: If the keyword arguments are not acceptable for
                `datetime.datetime.replace`.
        """
        # Use datetime.replace for its assertions
        datetime.now().replace(**kwargs)
        self._kwargs = kwargs

    def replace(self, sourceTime):
        """Perform the replacement on the given ``datetime``.

        Args:
            sourceTime (datetime.datetime): The date to use as a source for
                replacement.

        Returns:
            datetime.datetime: A copy of the ``sourceTime`` modified according
            to the replacement rules.
        """
        return sourceTime.replace(**self._kwargs)

    @classmethod
    def fromWildcardString(cls, wildcardString):
        """Converts a string in *yyyy-mm-dd HH:MM:SS* format to a
        `dateReplacement`.

        Any field that should not be modified should be marked with an ``x``
        and any field denoted with a number will be used for replacement. For
        example, to convert a date to January without affecting the year, day,
        or time the ``wildcardString`` should be ``xxxx-01-xx xx:xx:xx``. A
        field cannot be partially replaced; ``19xx-xx-xx xx:xx:xx`` will make
        no changes to the ``sourceTime`` since the year was not fully
        specified.

        Args:
            wildcardString (str): A string in *yyyy-mm-dd HH:MM:SS* format with
                numbers in any field that should be replaced.

        Returns:
            dateReplacement: The `dateReplacement` instance capable of making
            the replacement identified in the `wildcardString`.

        Raises:
            ValueError: If the `wildcardString` is not properly formatted.
        """
        components = re.split(r'[:-]| +', wildcardString)
        keywords = ('year', 'month', 'day', 'hour', 'minute', 'second')
        kwargs = {}

        if len(components) != 6:
            raise ValueError('invalid dateReplacement string: %s' %
                             wildcardString)

        for index, kw in enumerate(keywords):
            if components[index].isdigit():
                kwargs[kw] = int(components[index])

        return dateReplacement(**kwargs)
    
    def __eq__(self, other):
        if isinstance(other, dateReplacement):
            return self._kwargs == other._kwargs
        return NotImplemented


class nlpTarget(object):
    """Represents one or more dates and phrases that would be parsed from a
    source phrase by `nlp`.
    """
    def __init__(self, targets, testCase=None, sourcePhrase=None):
        """Initializes an `nlpTarget`.

        Args:
            targets (List[Dict[str,Any]]): A list of dictionaries with keys
                corresponding to keyword arguments of `nlpTargetValue`. There
                may be no additional keys and all input is type-validated with
                assertions.
            sourcePhrase (str): The phrase on which `nlp` will operate.
            testCase (TestCase): The `TestCase` to use for resolving targets.

        Raises:
            AssertionError: If any input is of the incorrect type.
        """
        self._targets = targets
        self._targetValues = [nlpTargetValue(**target) for target in targets]
        self._testCase = testCase
        self.sourcePhrase = sourcePhrase

    def forTestCase(self, testCase, sourcePhrase):
        return nlpTarget(self._targets, testCase, sourcePhrase)

    @property
    def testCase(self):
        return self._testCase

    @property
    def sourcePhrase(self):
        return self._sourcePhrase

    @sourcePhrase.setter
    def sourcePhrase(self, sourcePhrase):
        self._sourcePhrase = sourcePhrase

    @property
    def tupleValue(self):
        """Union[None,Tuple[Tuple[datetime.datetime,pdtContext,int,int,str]]]:
        The expected result from ``calendar.nlp(sourcePhrase, sourceTime)``

        Raises:
            ValueError: If `testCase` or `sourcePhrase` are not yet set.
            ValueError: If any of the target values include a phrase that is
                not contained in `sourcePhrase`.
        """
        values = []

        if self.testCase is None:
            raise ValueError('testCase must be specified to generate a ' +
                             'tupleValue')
        if self.sourcePhrase is None:
            raise ValueError('sourcePhrase must be specified to generate a ' +
                             'tupleValue')

        for targetValue in self._targetValues:
            if targetValue.target is None:
                continue
            startIndex = targetValue.startIndex
            target = self.testCase.resolveTarget(targetValue.target)
            if startIndex is None:
                if targetValue.phrase not in self.sourcePhrase:
                    raise ValueError('The phrase %r is not contained in %r' % (
                                     targetValue.phrase, self.sourcePhrase))
                startIndex = self.sourcePhrase.index(targetValue.phrase)
            endIndex = startIndex + len(targetValue.phrase)
            values.append((target, targetValue.context, startIndex, endIndex,
                           targetValue.phrase))

        return tuple(values) or None

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, self.tupleValue)

    def __eq__(self, other):
        """Allows an `nlpTarget` to be compared directly to the tuple returned
        by `nlp`.

        Args:
            other (Union[tuple, nlpTarget]): The object to test for equality.

        Returns:
            bool: Whether the objects compared both represent the same value.
        """
        if other is None:
            return self.tupleValue is None
        if isinstance(other, tuple):
            return self.tupleValue == other
        if isinstance(other, nlpTarget):
            return self.tupleValue == other.tupleValue
        return NotImplemented


class nlpTargetValue(object):
    """An immutable container structure for representing a single value in the
    tuple format created by `nlp`.
    """
    def __init__(self, phrase, target, context=None, startIndex=None):
        """Initializes an `nlpTargetValue`

        Args:
            phrase (str): The phrase matched by `nlp`.
            target (Union[datetime.datetime,datedelta]): The date represented
                by the phrase.
            context (Optional[pdtContext]): The context representing the
                phrase. If not specified, the wildcard context will be used to
                match any context.
            startIndex (Optional[int]): The index of the phrase as it appears
                in the source phrase. The end index is always calculated
                automatically based on the length of the phrase.
        """
        if not isinstance(phrase, basestring):
            raise TypeError('unsupported type for nlpTargetValue phrase' %
                            type(phrase).__name__)
        if not isinstance(context, (pdtContext, type(None))):
            raise TypeError('unsupported type for nlpTargetValue context: %s' %
                            type(context).__name__)
        if not isinstance(startIndex, (int, long, type(None))):
            raise TypeError('unsupported type for nlpTargetValue startIndex' %
                            type(startIndex).__name__)

        self._phrase = phrase
        self._target = target
        self._context = context or pdtContext(pdtContext.ACU_WILDCARD)
        self._startIndex = startIndex

    @property
    def phrase(self):
        return self._phrase

    @property
    def target(self):
        return self._target

    @property
    def context(self):
        return self._context

    @property
    def startIndex(self):
        return self._startIndex


class TestGroup(object):
    """Parses a test group configuration to prepare for parametrizing a test.
    """
    def __init__(self, groupData, localeID):
        """Initializes a `TestGroup`. `TestCase` instances are not created
        until the `parameterValues` are requested.

        Args:
            groupData (Dict): The data for a group of related tests. Supported
                top-level keys are:

                sourceTime
                    An optional way to specify or modify the datetimes against
                    which the test will be run. By default, the test will be
                    run against a small set of dates focusing on leap days and
                    similar edge cases. Specify a `dateReplacement` to modify
                    those dates, for example to ensure the month is January. A
                    list of dates can be provided as an alternative to the
                    default dates, which is particularly useful when dates must
                    fall on a specific day of the week. While a single
                    `datetime.datetime` can be provided, it is recommended to
                    specify at least two values for ``sourceTime`` if the
                    defaults cannot be used.
                options
                    A dictionary mapping `Constants` attribute names to the
                    value that should be set when running a test. This is
                    useful for modifying flags such as StartTimeFromSourceTime
                    or DOWParseStyle.
                cases
                    A list of objects suitable for creating `TestCase`. Cases
                    are usually grouped by target and context so that multiple
                    phrases with the same target date and context flags appear
                    in a single case.
            localeID (str): The locale from which the test data was loaded.
        """
        # TODO: Constants and Calendar options in test data
        constants = Constants(localeID, usePyICU=False)
        sourceTime = groupData.get('sourceTime')
        options = groupData.get('options') or {}
        calendar_options = {}

        for (attr, value) in options.items():
            if attr == 'day_start_hour':
                calendar_options[attr] = value
            else:
                setattr(constants, attr, value)

        self._calendar = Calendar(constants, version=VERSION_CONTEXT_STYLE, **calendar_options)
        self._caseData = groupData['cases']
        self._sourceTimes = DEFAULT_SOURCE_TIMES

        if isinstance(sourceTime, dateReplacement):
            self._sourceTimes = [sourceTime.replace(dt)
                                 for dt in self._sourceTimes]
        elif isinstance(sourceTime, list):
            self._sourceTimes = sourceTime
        elif sourceTime is not None:
            self._sourceTimes = [sourceTime]

    @property
    def calendar(self):
        return self._calendar

    @property
    def sourceTimes(self):
        return self._sourceTimes

    @classmethod
    def supportedParameters(self, parameters):
        """Filters the given parameters returning a list of those supported by
        a test group.

        Args:
            parameters (List[str]): A list of function parameter names, some of
                which may be pytest fixtures, others may be provided by
                testGroup parametrization.

        Returns:
            List[str]: The parameters that are supported by testGroup
            parametrization.
        """
        return [p for p in parameters if p in _PROPERTY_MAPPING]

    def parameterValues(self, parameters):
        """Gather all values for the specified parameters across all cases in
        the test group.

        Args:
            parameters (List[str]): The parameters that will be injected into
                the test function. Supported parameters are  ``sourceTime``,
                ``target``, ``phrase``, ``context``, ``calendar``, and
                ``nlpTarget``.

        Returns:
            List[Tuple]: A list of tuples containing values that correspond to
            the order of the `parameters`.
        """
        values = []
        for sourceTime in self.sourceTimes:
            for caseData in self._caseData:
                case = TestCase(caseData, self.calendar, sourceTime)
                values.extend(case.parameterValues(parameters))

        return values


class TestCase(object):
    """Represents a single test case within a group, resolving test data
    according to the group and case configuration.
    """
    def __init__(self, caseData, calendar, sourceTime):
        self._calendar = calendar
        self._sourceTime = sourceTime
        self._phrases = caseData['phrases']
        self._target = caseData.get('target')
        self._context = (caseData.get('context') or
                         pdtContext(pdtContext.ACU_WILDCARD))

        if 'sourceTime' in caseData:
            self._sourceTime = self.resolveTime(caseData['sourceTime'])

    @property
    def calendar(self):
        return self._calendar

    @property
    def context(self):
        return self._context

    @property
    def sourceTime(self):
        return self._sourceTime

    @property
    def targetByPhrase(self):
        """Resolves the target value for each phrase.

        Returns:
            Dict[str, Any]: A dictionary mapping phrases to the target
            specified in the test data. In most cases the target is either a
            `datetime.datetime` or ``None``.
        """
        phrases = {}
        if isinstance(self._phrases, list):
            for phrase in self._phrases:
                target = self.resolveTarget(self._target, phrase)
                phrases[phrase] = target
        if isinstance(self._phrases, dict):
            for phrase, target in self._phrases.items():
                phrases[phrase] = self.resolveTarget(target, phrase)
        return phrases

    def resolveTime(self, value):
        """Uses the case's `sourceTime` to resolve date replacements and
        deltas to explicit `datetime.datetime` values.

        Args:
            value (Union[datetime.datetime, dateReplacement, datedelta]):
                The value to resolve.

        Returns:
            datetime.datetime: The explicit `datetime.datetime` to which the
            `value` mapped in the context of the `sourceTime`.
        """
        if isinstance(value, datetime):
            return value
        if isinstance(value, dateReplacement):
            return value.replace(self.sourceTime)
        if isinstance(value, datedelta):
            sourceTime = self.resolveTime(value.sourceTime)
            return value.add(sourceTime, self.calendar)
        return self.sourceTime

    def resolveTarget(self, value, phrase=None):
        """Ensures that the target is ready for use in a test assertion.

        Resolves `dateReplacement` and `datedelta` to an explicit
        `datetime.datetime` and prepares `nlpTarget` values for comparison to
        `nlp` return values.

        Args:
            value (Any): The value to resolve.
            phrase (Optional[str]): The phrase with which the target is
                associated for use with resolving `nlpTarget` values.

        Returns:
            Any: The resolved value, or the provided value if not of a type
            that requires resolution.
        """
        if isinstance(value, (dateReplacement, datedelta)):
            return self.resolveTime(value)
        if isinstance(value, list):
            return [self.resolveTarget(item, phrase) for item in value]
        if isinstance(value, nlpTarget):
            return value.forTestCase(self, phrase)
        return value

    def nlpTarget(self, value, phrase):
        """Coerces the `value` to an `nlpTarget` then resolves that target to
        prepare for testing.

        Args:
            value (Any): A test target value.
            phrase (str): The phrase with which the target is associated.

        Returns:
            nlpTarget: An `nlpTarget` that is prepared to compare against the
            return value of `nlp`.
        """
        if not isinstance(value, nlpTarget):
            value = nlpTarget(targets=[{
                'target': value,
                'context': self.context,
                'phrase': phrase
            }])
        return self.resolveTarget(value, phrase)

    def parameterValues(self, parameters):
        """Collects the values corresponding to each parameter from the test
        data.

        Args:
            parameters (List[str]): The parameters that will be injected into
                the test function.

        Returns:
            Tuple: A tuple containing values that correspond to the order of
            the `parameters`.
        """
        values = []
        for phrase, target in self.targetByPhrase.items():
            phraseValues = []
            for parameter in parameters:
                if parameter in _PROPERTY_MAPPING:
                    value = _PROPERTY_MAPPING[parameter](self, target, phrase)
                    phraseValues.append(value)
            # Individual parameters must be unwrapped otherwise a tuple
            # containing the value is injected in the test
            if len(phraseValues) == 1:
                values.append(phraseValues[0])
            else:
                values.append(tuple(phraseValues))

        return tuple(values)
