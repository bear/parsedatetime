# -*- coding: utf-8 -*-
"""
Processes YAML data files with extensions specific to parsedatetime.

In addition to the syntax supported by ``PyYaml``, this module provides a few
constructors to represent parsedatetime and test constructs in YAML.
"""

import re
import yaml

from parsedatetime.context import pdtContext
from tests.lib.models import datedelta, dateReplacement, nlpTarget
from tests import log


def loadData(path):
    """Load YAML data from the specified path, memoizing the most recently
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
                raise exc

    return data


loadData._cache = {}


def datedeltaConstructor(loader, node):
    """A YAML constructor for representing time and date deltas relative to a source time.

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


def dateReplacementConstructor(loader, node):
    """A YAML constructor for representing `dateReplacement` instances.

    In some cases it is necessary to replace a component of a
    `datetime.datetime` in a way that cannot be done with `datedelta`. This
    constructor provides a simple format for identifying portions of a datetime
    to replace.

    Avoid creating impossible dates! February, April, June, September and
    November should be avoided since they could result in an invalid date like
    April 31.

    Examples:
        To convert any date to January::

            !replace xxxx-01-xx xx:xx:xx

        To set the hour and minute for any datetime::

            !replace xxxx-xx-xx 12:34:xx

    Args:
        loader (yaml.Loader): The YAML loader
        node (yaml.ScalarNode): The value provided to the ``!replace``
            constructor, unwrappable by `loader` as a scalar value

    Returns:
        dateReplacement: The `dateReplacement` corresponding to the scalar
        value as returned by `dateReplacement.fromWildcardString`.
    """
    value = loader.construct_scalar(node)
    return dateReplacement.fromWildcardString(value)


def nlpTargetConstructor(loader, node):
    """A YAML constructor for representing `nlpTarget` instances.

    Test cases expecting to be evaluated against `Calendar.nlp` can fully (or
    partially, for convenience) specify the components of its return value in
    the test data. The resulting `nlpTarget` can be compared against the tuple
    returned by `nlp` with a simple equality assertion.

    The context and startIndex values are optional; providing a context
    improves the quality of a test but startIndex *should only be used* if the
    source phrase contains the same date phrase multiple times. Specifying a
    startIndex reduces the reusability of tests cases (e.g. wrapping the phrase
    in quotes).

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
yaml.add_constructor(u'!replace', dateReplacementConstructor)
yaml.add_constructor(u'!nlpTarget', nlpTargetConstructor)
yaml.add_constructor(u'!pdtContext', pdtContextConstructor)
