# -*- coding: utf-8 -*-
#
# vim: sw=2 ts=2 sts=2
#
# Copyright 2004-2021 Mike Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""parsedatetime.parsing.units — unit-based time parsing

Contains:
- _matchUnits / _applyUnits    — quantity + units (5 hours, 3 days)
- _matchQUnits / _applyQUnits  — quantity + short units (5h, 3d)
- _UnitsTrapped                — detect day suffix trapped by unit match
"""

from __future__ import with_statement, absolute_import, unicode_literals

import time
import logging
import datetime

from ..context import pdtContext
from ..time_utils import _buildTime

debug = False


def _UnitsTrapped(ptc, s, m, key):
    """Check if a day suffix got trapped by a unit match.

    For example Dec 31st would match for 31s (aka 31 seconds)
    Dec 31st
        ^ ^
        | +-- m.start('units')
        |     and also m2.start('suffix')
        +---- m.start('qty')
              and also m2.start('day')
    """
    m2 = ptc.CRE_DAY2.search(s)
    if m2 is not None:
        t = '%s%s' % (m2.group('day'), m.group(key))
        if m.start(key) == m2.start('suffix') and \
                m.start('qty') == m2.start('day') and \
                m.group('qty') == t:
            return True
        else:
            return False
    else:
        return False


def _applyUnits(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchUnits()}.
    Renamed from _evalUnits for clarity.
    """
    from ..time_utils import _parse_date_rfc822, _parse_date_w3dtf

    ptc = calendar.ptc
    s = datetimeString.strip()

    # Try RFC822 / W3CDTF first
    if sourceTime is None:
        sourceTime = _parse_date_rfc822(s)
        debug and logging.debug(
            'attempt to parse as rfc822 - %s', str(sourceTime))

        if sourceTime is not None:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst, _) = sourceTime
            calendar.currentContext.updateAccuracy(
                pdtContext.ACU_YEAR, pdtContext.ACU_MONTH, pdtContext.ACU_DAY)

            if hr != 0 and mn != 0 and sec != 0:
                calendar.currentContext.updateAccuracy(
                    pdtContext.ACU_HOUR, pdtContext.ACU_MIN, pdtContext.ACU_SEC)

            sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

    if sourceTime is None:
        sourceTime = _parse_date_w3dtf(s)

        if sourceTime is not None:
            calendar.currentContext.updateAccuracy(
                pdtContext.ACU_YEAR, pdtContext.ACU_MONTH, pdtContext.ACU_DAY,
                pdtContext.ACU_HOUR, pdtContext.ACU_MIN, pdtContext.ACU_SEC)

    if sourceTime is None:
        sourceTime = time.localtime()

    # Given string is a time string with units like "5 hrs 30 min"
    modifier = ''  # TODO

    m = ptc.CRE_UNITS.search(s)
    if m is not None:
        units = m.group('units')
        quantity = s[:m.start('units')]

    sourceTime = _buildTime(calendar, sourceTime, quantity, modifier, units)
    return sourceTime


def _applyQUnits(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchQUnits()}.
    Renamed from _evalQUnits for clarity.
    """
    from ..time_utils import _parse_date_rfc822, _parse_date_w3dtf

    ptc = calendar.ptc
    s = datetimeString.strip()

    # Try RFC822 / W3CDTF first
    if sourceTime is None:
        sourceTime = _parse_date_rfc822(s)
        debug and logging.debug(
            'attempt to parse as rfc822 - %s', str(sourceTime))

        if sourceTime is not None:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst, _) = sourceTime
            calendar.currentContext.updateAccuracy(
                pdtContext.ACU_YEAR, pdtContext.ACU_MONTH, pdtContext.ACU_DAY)

            if hr != 0 and mn != 0 and sec != 0:
                calendar.currentContext.updateAccuracy(
                    pdtContext.ACU_HOUR, pdtContext.ACU_MIN, pdtContext.ACU_SEC)

            sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

    if sourceTime is None:
        sourceTime = _parse_date_w3dtf(s)

        if sourceTime is not None:
            calendar.currentContext.updateAccuracy(
                pdtContext.ACU_YEAR, pdtContext.ACU_MONTH, pdtContext.ACU_DAY,
                pdtContext.ACU_HOUR, pdtContext.ACU_MIN, pdtContext.ACU_SEC)

    if sourceTime is None:
        sourceTime = time.localtime()

    # Given string is a time string with single char units like "5 h 30 m"
    modifier = ''  # TODO

    m = ptc.CRE_QUNITS.search(s)
    if m is not None:
        units = m.group('qunits')
        quantity = s[:m.start('qunits')]

    sourceTime = _buildTime(calendar, sourceTime, quantity, modifier, units)
    return sourceTime


def _matchUnits(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_UNITS, used by L{Calendar.parse()}.
    Renamed from _partialParseUnits for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # Quantity + Units
    m = ptc.CRE_UNITS.search(s)
    if m is not None:
        debug and logging.debug('CRE_UNITS matched')
        if _UnitsTrapped(ptc, s, m, 'units'):
            debug and logging.debug('day suffix trapped by unit match')
        else:
            if (m.group('qty') != s):
                # capture remaining string
                parseStr = m.group('qty')
                chunk1 = s[:m.start('qty')].strip()
                chunk2 = s[m.end('qty'):].strip()

                if chunk1[-1:] == '-':
                    parseStr = '-%s' % parseStr
                    chunk1 = chunk1[:-1]

                s = '%s %s' % (chunk1, chunk2)
            else:
                parseStr = s
                s = ''

    if parseStr:
        debug and logging.debug(f'found (units) [{parseStr}][{chunk1}][{chunk2}]')
        sourceTime = _applyUnits(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)


def _matchQUnits(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_QUNITS, used by L{Calendar.parse()}.
    Renamed from _partialParseQUnits for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # Quantity + Units
    m = ptc.CRE_QUNITS.search(s)
    if m is not None:
        debug and logging.debug('CRE_QUNITS matched')
        if _UnitsTrapped(ptc, s, m, 'qunits'):
            debug and logging.debug('day suffix trapped by qunit match')
        else:
            if (m.group('qty') != s):
                # capture remaining string
                parseStr = m.group('qty')
                chunk1 = s[:m.start('qty')].strip()
                chunk2 = s[m.end('qty'):].strip()

                if chunk1[-1:] == '-':
                    parseStr = '-%s' % parseStr
                    chunk1 = chunk1[:-1]

                s = '%s %s' % (chunk1, chunk2)
            else:
                parseStr = s
                s = ''

    if parseStr:
        debug and logging.debug(f'found (qunits) [{parseStr}][{chunk1}][{chunk2}]')
        sourceTime = _applyQUnits(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)
