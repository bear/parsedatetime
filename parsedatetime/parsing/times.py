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

"""parsedatetime.parsing.times — time parsing

Contains:
- _matchTimeStr / _applyTimeStr  — natural language time strings (lunch, midnight, now, etc.)
- _matchMeridian / _applyMeridian — HH:MM(:SS) am/pm time strings
- _matchTimeStd / _applyTimeStd  — HH:MM(:SS) standard time strings
"""

from __future__ import with_statement, absolute_import, unicode_literals

import time
import logging
import datetime

from ..context import pdtContext
from ..time_utils import _extract_time, _pop_time_accuracy

debug = False


def _applyTimeStr(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchTimeStr()}.
    Renamed from _evalTimeStr for clarity.
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

    if s in ptc.re_values['now']:
        calendar.currentContext.updateAccuracy(pdtContext.ACU_NOW)
    else:
        # Given string is a natural language time string like
        # lunch, midnight, etc
        sTime = ptc.getSource(s, sourceTime)
        if sTime:
            sourceTime = sTime
        calendar.currentContext.updateAccuracy(pdtContext.ACU_HALFDAY)

    return sourceTime


def _applyMeridian(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchMeridian()}.
    Renamed from _evalMeridian for clarity.
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

    # Given string is in the format HH:MM(:SS)(am/pm)
    yr, mth, dy, hr, mn, sec, wd, yd, isdst = sourceTime

    m = ptc.CRE_TIMEHMS2.search(s)
    if m is not None:
        dt = s[:m.start('meridian')].strip()
        if len(dt) <= 2:
            hr = int(dt)
            mn = 0
            sec = 0
        else:
            hr, mn, sec = _extract_time(m)

        if hr == 24:
            hr = 0

        meridian = m.group('meridian').lower()

        # if 'am' found and hour is 12 - force hour to 0 (midnight)
        if (meridian in ptc.am) and hr == 12:
            hr = 0

        # if 'pm' found and hour < 12, add 12 to shift to evening
        if (meridian in ptc.pm) and hr < 12:
            hr += 12

    # time validation
    if hr < 24 and mn < 60 and sec < 60:
        sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
        _pop_time_accuracy(m, calendar.currentContext)

    return sourceTime


def _applyTimeStd(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchTimeStd()}.
    Renamed from _evalTimeStd for clarity.
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

    # Given string is in the format HH:MM(:SS)
    yr, mth, dy, hr, mn, sec, wd, yd, isdst = sourceTime

    m = ptc.CRE_TIMEHMS.search(s)
    if m is not None:
        hr, mn, sec = _extract_time(m)
    if hr == 24:
        hr = 0

    # time validation
    if hr < 24 and mn < 60 and sec < 60:
        sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
        _pop_time_accuracy(m, calendar.currentContext)

    return sourceTime


def _matchTimeStr(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_TIME, used by L{Calendar.parse()}.
    Renamed from _partialParseTimeStr for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # Natural language time strings
    m = ptc.CRE_TIME.search(s)
    if m is not None or s in ptc.re_values['now']:

        if (m and m.group() != s):
            # capture remaining string
            parseStr = m.group()
            chunk1 = s[:m.start()]
            chunk2 = s[m.end():]
            s = '%s %s' % (chunk1, chunk2)
        else:
            parseStr = s
            s = ''

    if parseStr:
        debug and logging.debug(
            'found (time) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyTimeStr(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)


def _matchMeridian(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_TIMEHMS2, used by L{Calendar.parse()}.
    Renamed from _partialParseMeridian for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # HH:MM(:SS) am/pm time strings
    if ptc.locale.usesMeridian:
        m = ptc.CRE_TIMEHMS2.search(s)
        if m is not None:
            if m.group('minutes') is not None:
                if m.group('seconds') is not None:
                    parseStr = '%s:%s:%s' % (m.group('hours'),
                                             m.group('minutes'),
                                             m.group('seconds'))
                else:
                    parseStr = '%s:%s' % (m.group('hours'),
                                          m.group('minutes'))
            else:
                parseStr = m.group('hours')
            parseStr += ' ' + m.group('meridian')

            chunk1 = s[:m.start()]
            chunk2 = s[m.end():]

            s = '%s %s' % (chunk1, chunk2)

        if parseStr:
            debug and logging.debug(f'found (meridian) [{parseStr}][{chunk1}][{chunk2}]')
            sourceTime = _applyMeridian(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)


def _matchTimeStd(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_TIMEHMS, used by L{Calendar.parse()}.
    Renamed from _partialParseTimeStd for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # HH:MM(:SS) time strings
    m = ptc.CRE_TIMEHMS.search(s)
    if m is not None:

        if m.group('seconds') is not None:
            parseStr = '%s:%s:%s' % (m.group('hours'),
                                     m.group('minutes'),
                                     m.group('seconds'))
            chunk1 = s[:m.start('hours')]
            chunk2 = s[m.end('seconds'):]
        else:
            parseStr = '%s:%s' % (m.group('hours'),
                                  m.group('minutes'))
            chunk1 = s[:m.start('hours')]
            chunk2 = s[m.end('minutes'):]

        s = '%s %s' % (chunk1, chunk2)

    if parseStr:
        debug and logging.debug(
            'found (hms) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyTimeStd(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)
