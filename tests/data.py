# -*- coding: utf-8 -*-
"""
Processes YAML data files with extensions specific to parsedatetime.

In addition to the syntax supported by ``PyYaml``, parsedatetime provides a few
constructors to represent data in YAML.
"""

from datetime import datetime, timedelta
import re
from warnings import warn
import yaml

from parsedatetime import Calendar
from parsedatetime.context import pdtContext
from tests import log


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

    Once the `calendar` has been set, the `datedelta` can be added to or
    subtracted from a `datetime.datetime`.
    """
    calendar = None
    sourceTime = None

    def __init__(self, years=0, months=0, sourceTime=None, calendar=None,
                 **kwargs):
        """Initialize a `datedelta`

        Args:
            years (Optional[int]): Number of years.
            months (Optional[int]): Number of months.
            sourceTime (Optional[datetime.datetime]): The date relative to
                which this `datedelta` should be interpreted.
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

        self._years = years
        self._months = months
        self.sourceTime = sourceTime
        self.calendar = calendar
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
        """datetime.datetime: The date relative to which this `datedelta`
            should always be interpreted. It is expected that any logic
            operating on a `datedelta` will check whether the `datedelta` has a
            `sourceTime` and if so, calculate a final date based on that rather
            than some other time.

        Raises:
            TypeError: If set to a value of the wrong type.
        """
        return self._sourceTime

    @sourceTime.setter
    def sourceTime(self, sourceTime):
        if not isinstance(sourceTime, (datetime, type(None))):
            raise TypeError('unsupported type for datedelta %s: %s' %
                            ('sourceTime', type(sourceTime).__name__))
        self._sourceTime = sourceTime

    @property
    def calendar(self):
        """parsedatetime.Calendar: The calendar on which `Calendar.inc` will be
        called to handle year and month calculation.

        Raises:
            TypeError: If set to a value of the wrong type.
        """
        return self._calendar

    @calendar.setter
    def calendar(self, calendar):
        if not isinstance(calendar, (Calendar, type(None))):
            raise TypeError('unsupported type for datedelta %s: %s' %
                            ('calendar', type(calendar).__name__))
        self._calendar = calendar

    def __add__(self, other):
        """Allows the `datedelta` to be added to a `datetime.datetime` value.

        Addition is not implemented for other types. Note that if the
        `datedelta` has a `sourceTime` set, this date should be used instead of
        a date specified elsewhere in the test data.

        The `datedelta` may appear on either side of the addition operator.

        Args:
            other (datetime.datetime): The date to adjust according to the
                delta.

        Returns:
            datetime.datetime: The adjusted date.

        Raises:
            ValueError: If the `calendar` has not yet been set.
        """
        if isinstance(other, datetime):
            if self.calendar is None:
                raise ValueError(
                    'Calendar must be set before operating on datedelta')
            if self.sourceTime and self.sourceTime != other:
                print self.sourceTime
                print other
                warn('datedelta was added to a datetime that did not match ' +
                     'its sourceTime')
            return self.calendar.inc(other, self._months, self._years) + \
                self._timedelta
        return NotImplemented

    __radd__ = __add__

    def __rsub__(self, other):
        """Allows the `datedelta` to be subtracted from a `datetime.datetime`
        value.

        Subtraction is not implemented for other types. Note that if the
        `datedelta` has a `sourceTime` set, this date should be used instead of
        a date specified elsewhere in the test data.

        The `datedelta` may only appear on the right side of the subtraction
        operator.

        Args:
            other (datetime.datetime): The date to adjust according to the
                delta.

        Returns:
            datetime.datetime: The adjusted date.

        Raises:
            ValueError: If the `calendar` has not yet been set.
        """
        if isinstance(other, datetime):
            if self.calendar is None:
                raise ValueError(
                    'Calendar must be set before operating on datedelta')
            if self.sourceTime and self.sourceTime != other:
                warn('datedelta was subtracted from a datetime that did not ' +
                     'match its sourceTime')
            return self.calendar.inc(other, -self._months, -self._years) - \
                self._timedelta
        return NotImplemented

    def __neg__(self):
        negkwargs = dict([(k, -v) for k, v in self._kwargs.items()])
        return self.__class__(-self.years, -self.months, **negkwargs)

    def __repr__(self):
        if self._years:
            return "%s(%d, %d, %s)" % (self.__class__.__name__,
                                       self._years,
                                       self._months,
                                       self._timedelta)
        if self._months:
            return "%s(%d, %s)" % (self.__class__.__name__,
                                   self._months,
                                   self._timedelta)

        return "%s(%s)" % (self.__class__.__name__, self._timedelta)

    def __str__(self):
        def plural(n):
            return n, abs(n) != 1 and "s" or ""
        s = ''
        if self._years:
            s += '%d year%s' % plural(self._years)
        if self._months:
            s += '%d month%s' % plural(self._months)

        return '%s %s' % (s, self._timedelta)


class nlpTarget(object):
    """Represents one or more dates and phrases that would be parsed from a
    source phrase by `nlp`.
    """

    def __init__(self, targets, calendar=None, sourceTime=None,
                 sourcePhrase=None):
        """Initializes an `nlpTarget`.

        Args:
            targets (List[Dict[str,Any]]): A list of dictionaries with keys
                corresponding to keyword arguments of `nlpTargetValue`. There
                may be no additional keys and all input is type-validated with
                assertions.
            calendar (Optional[parsedatetime.Calendar]): The calendar under
                which the phrase will be interpreted.
            sourcePhrase (Optional[str]): The phrase on which `nlp` will
                operate.
            sourceTime (Optional[datetime.datetime]): The date and time to
                which the test case is relative.

        Raises:
            AssertionError: If any input is of the incorrect type.
        """
        self._targetValues = tuple([nlpTargetValue(self, **t)
                                    for t in targets])
        self.calendar = calendar
        self.sourceTime = sourceTime
        self.sourcePhrase = sourcePhrase

    @property
    def calendar(self):
        """parsedatetime.Calendar: The calendar under which the phrase
        will be interpreted.

        Raises:
            TypeError: If set to a value not of type `Calendar`
        """
        return self._calendar

    @calendar.setter
    def calendar(self, calendar):
        if not isinstance(calendar, (Calendar, type(None))):
            raise TypeError('unsupported type for nlpTarget calendar: %s' %
                            type(calendar).__name__)

        self._calendar = calendar

    @property
    def sourceTime(self):
        """datetime.datetime: The date and time to which the test
        case is relative.

        Raises:
            AssertionError: If set to a value not of type `datetime.datetime`
        """
        return self._sourceTime

    @sourceTime.setter
    def sourceTime(self, sourceTime):
        if not isinstance(sourceTime, (datetime, type(None))):
            raise TypeError('unsupported type for nlpTarget sourceTime: %s' %
                            type(sourceTime).__name__)

        self._sourceTime = sourceTime

    @property
    def sourcePhrase(self):
        """str: The phrase on which `nlp` will operate.

        Raises:
            AssertionError: If set to a value not of type `basestring`
        """
        return self._sourcePhrase

    @sourcePhrase.setter
    def sourcePhrase(self, sourcePhrase):
        if not isinstance(sourcePhrase, (basestring, type(None))):
            raise TypeError('unsupported type for nlpTarget sourcePhrase: %s' %
                            type(sourcePhrase).__name__)

        self._sourcePhrase = sourcePhrase

    @property
    def tupleValue(self):
        """Tuple[Tuple[datetime.datetime,pdtContext,int,int,str]]: The
        expected result from ``calendar.nlp(sourcePhrase, sourceTime)``

        Raises:
            ValueError: If `calendar`, `sourceTime`, or `sourcePhrase` are not
                yet set.
            ValueError: If any of the target values include a phrase that is
                not contained in `sourcePhrase`.
        """
        if self.calendar is None:
            raise ValueError('The calendar has not yet been set')
        if self.sourceTime is None:
            raise ValueError('The sourceTime has not yet been set')
        if self.sourcePhrase is None:
            raise ValueError('The sourcePhrase has not yet been set')
        return tuple([t.tupleValue for t in self._targetValues])

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, self.tupleValue)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.tupleValue == other
        if isinstance(other, nlpTarget):
            return self.tupleValue == other.tupleValue
        return NotImplemented


class nlpTargetValue(object):
    """An immutable container structure for representing a single value in the
    tuple format created by `nlp`.
    """
    def __init__(self, parent, phrase, target, context=None, startIndex=None):
        """Initializes an `nlpTargetValue`

        Args:
            parent (nlpTarget): The target from which this value was
                constructed.
            phrase (str): The phrase matched by `nlp`.
            target (Union[datetime.datetime,datedelta]): The date represented
                by the phrase.
            context (Optional[pdtContext]): The context representing the
                phrase.
            startIndex (Optional[int]): The index of the phrase as it appears
                in the source phrase. The end index is always calculated
                automatically based on the length of the phrase.
        """
        if not isinstance(parent, nlpTarget):
            raise TypeError('unsupported type for nlpTargetValue parent: %s' %
                            type(context).__name__)
        if not isinstance(phrase, basestring):
            raise TypeError('unsupported type for nlpTargetValue phrase' %
                            type(phrase).__name__)
        if not isinstance(context, (pdtContext, type(None))):
            raise TypeError('unsupported type for nlpTargetValue context: %s' %
                            type(context).__name__)
        if not isinstance(startIndex, (int, long, type(None))):
            raise TypeError('unsupported type for nlpTargetValue startIndex' %
                            type(startIndex).__name__)

        self._parent = parent
        self._phrase = phrase
        self._target = target
        self._context = context
        self._startIndex = startIndex

    @property
    def tupleValue(self):
        """Tuple[datetime.datetime,pdtContext,int,int,str]: A phrase tuple as
        returned by `nlp`. The tuple contains the `datetime.datetime`, the
        `pdtContext` representing the phrase, the start and end indexes of the
        phrase within the source phrase, and the phrase.

        Raises:
            AssertionError: If the `nlpTargetValue` phrase is not included in
                the `nlpTarget` `sourcePhrase`.
        """
        context = self._context or pdtContext(pdtContext.ACU_WILDCARD)
        startIndex = self._startIndex
        target = self._target
        if startIndex is None:
            if self._phrase not in self._parent.sourcePhrase:
                raise ValueError('The phrase %r is not contained in %r' % (
                                 self._phrase, self._parent.sourcePhrase))
            startIndex = self._parent.sourcePhrase.index(self._phrase)
        endIndex = startIndex + len(self._phrase)
        if isinstance(target, datedelta):
            target.calendar = self._parent.calendar
            target = self._parent.sourceTime + target
        return (target, context, startIndex, endIndex, self._phrase)

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, self.tupleValue)


def loadData(path):
    """
    Loads YAML data from the specified path, memoizing the most recently
    accessed file to avoid excessive IO.

    Args:
        path (str): Absolute path to a YAML file.

    Returns:
        Union[Dict, None]: Parsed contents of the file at `path` or `None` if
        the file could not be read.
    """
    data = None

    if path in loadData._cache:
        data = loadData._cache[path]
    else:
        with open(path, 'r') as stream:
            try:
                data = yaml.load(stream)
                # Purposely only keeping one in memory at a time
                loadData._cache = {
                    path: data
                }
            except yaml.YAMLError as exc:
                log.error(exc)

    return data

loadData._cache = {}


def datedeltaConstructor(loader, node):
    """A YAML constructor for representing time and date deltas relative to a
    source time.

    Unlike `datetime.timedelta`, this delta representation is interpreted
    relative to a source time and can therefore represent calendar-based year
    and month deltas via `Calendar.inc` in addition to the units supported by
    `datetime.timedelta`. The following keys are supported:

    * months
    * years
    * days
    * weeks
    * hours
    * minutes
    * seconds
    * milliseconds
    * microseconds
    * sourceTime

    Note that the ``sourceTime`` value should only be provided here if it
    differs from the ``sourceTime`` assigned to the test case. For example, to
    test that the phrase *4pm + 1d* works from a source time of *2016-02-28
    00:00:00*, it would be necessary to include *2016-02-28 16:00:00* as the
    ``sourceTime`` in the `datedelta` as shown in the examples below. While it
    is generally recommended to specify targets as explicit `datetime.datetime`
    values, in some cases this format makes the intent of the test more clear.

    Examples:
        Yesterday::

            !datedelta
                days: -1

        Next year (see `Calendar.inc`)::

            !datedelta
                years: 1

        1 year, 2 months, and 30 minutes from now::

            !datedelta
                years: 1
                months: 2
                minutes: 30

        4pm + 1d::

            !datedelta
                sourceTime: 2016-02-28 16:00:00
                days: 1

    Args:
        loader (yaml.Loader): The YAML loader
        node (yaml.MappingNode): The value provided to the ``!datedelta``
            constructor, unwrappable by `loader` as a dict

    Returns:
        datedelta: A value that can be added to or subtracted from a
        `datetime.datetime` to calculate an offset date.

    Raises:
        TypeError: If any parameters are unsupported or of the wrong type.
    """
    value = loader.construct_mapping(node)
    return datedelta(**value)


def nlpTargetConstructor(loader, node):
    """A YAML constructor for representing `nlpTarget` instances.

    Test cases expecting to be evaluated against `Calendar.nlp` can fully (or
    partially, for convenience) specify the components of its return value in
    the test data. The resulting `nlpTarget` can be compared against the tuple
    returned by `nlp` with a simple equality assertion.

    The context and startIndex values are optional; providing a context
    improves the quality of a test but startIndex is only required if the
    source phrase contains the same date phrase multiple times.

    Examples:
        Yesterday I went to the park at noon::

            !nlpTarget
                - phrase: "Yesterday"
                  context: !pdtContext day
                  target: !datedelta
                    days: -1
                - phrase: "at noon"
                  context: !pdtContext halfday
                  target: 2016-01-01 12:00:00

        Yep, today was as good as today could be::

            !nlpTarget
                - phrase: "today"
                  startIndex: 5
                  target: 2013-08-01 09:00:00
                - phrase: "today"
                  startIndex: 26
                  target: 2013-08-01 09:00:00

    Args:
        loader (yaml.Loader): The YAML loader
        node (yaml.SequenceNode): The value provided to the ``!nlpTarget``
            constructor, unwrappable by `loader` as a sequence value

    Returns:
        nlpTarget: A value that can be compared against the return value of
        `nlp`.

    Raises:
        TypeError: If any data is of the wrong type.
    """
    values = loader.construct_sequence(node, deep=True)
    return nlpTarget(values)


def pdtContextConstructor(loader, node):
    """A YAML constructor for representing `pdtContext` instances.

    `pdtContext` tracks the composition of a date phrase based on various
    components such as month, year, and hour. The accuracy can be specified in
    YAML by separating mulitple values with the pipe ``|`` character,
    reminiscent of the bitwise OR used to combine accuracy flags in python.
    Any value in `pdtContext._ACCURACY_REVERSE_MAPPING` may be used (or no
    value at all), though singular forms are preferred over plurals for
    consistency.

    Examples:
        2 days ago::

            !pdtContext day

        2 months, 1 hour, 4 minutes, 32 seconds::

            !pdtContext second | hour | month | minute

        Order does not matter, but to maintain consistency the flags should be
        listed in decreasing duration order::

            !pdtContext month | hour | minute | second

        Noon::

            !pdtContext halfday

        No date or time components::

            !pdtContext

    Args:
        loader (yaml.Loader): The YAML loader
        node (yaml.ScalarNode): The value provided to the ``!pdtContext``
            constructor, unwrappable by `loader` as a scalar value

    Returns:
        pdtContext: A context representing the specified accuracy values
    """
    value = loader.construct_scalar(node)
    accuracyStrings = re.split(r'\s*\|\s*', value)
    return pdtContext.fromAccuracyStrings(accuracyStrings)


yaml.add_constructor(u'!datedelta', datedeltaConstructor)
yaml.add_constructor(u'!nlpTarget', nlpTargetConstructor)
yaml.add_constructor(u'!pdtContext', pdtContextConstructor)
