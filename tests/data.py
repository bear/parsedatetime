# -*- coding: utf-8 -*-
"""
Processes YAML data files with extensions specific to parsedatetime.

In addition to the syntax supported by ``PyYaml``, parsedatetime provides a few
constructors to represent data in YAML.
"""

import re
import yaml

from parsedatetime.context import pdtContext
from tests import log

DATEDELTA_KEY = '__datedelta__'
"""A dictionary key to identify a date delta, in lieu of a `datedelta` class"""


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

    Currently these values are represented internally by a dict as provided in
    YAML with the addition of the special `DATEDELTA_KEY`.

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
        Dict[str, Union[int, float]]: A dict with `DATEDELTA_KEY`
        and any other `Calendar.inc` and `datetime.timedelta`
    """
    value = loader.construct_mapping(node)
    # TODO: datedelta class to wrap year and month deltas to avoid calling
    # Calendar.inc
    value[DATEDELTA_KEY] = True
    return value


def contextConstructor(loader, node):
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
yaml.add_constructor(u'!pdtContext', contextConstructor)
