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

"""parsedatetime.parsing.dates — date parsing

Contains:
- _matchDateStr / _applyDateStr  — long-form date strings (May 23rd, 2005)
- _matchDateStd / _applyDateStd  — short-form date strings (07/21/2006)
"""

from __future__ import with_statement, absolute_import, unicode_literals

import time
import logging
import datetime

from ..context import pdtContext

debug = False


def _applyDateStr(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchDateStr()}.
    Renamed from _evalDateStr for clarity.
    """
    from ..time_utils import _parse_date_rfc822, _parse_date_w3dtf

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

    # Given string is in the format  "May 23rd, 2005"
    debug and logging.debug('checking for MMM DD YYYY')
    return calendar.parseDateText(s, sourceTime)


def _applyDateStd(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchDateStd()}.
    Renamed from _evalDateStd for clarity.
    """
    from ..time_utils import _parse_date_rfc822, _parse_date_w3dtf

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

    # Given string is in the format 07/21/2006
    return calendar.parseDate(s, sourceTime)


def _matchDateStr(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_DATE3, used by L{Calendar.parse()}.
    Renamed from _partialParseDateStr for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    m = ptc.CRE_DATE3.search(s)

    # String date format
    if m is not None:

        if (m.group('date') != s):
            # capture remaining string
            mStart = m.start('date')
            mEnd = m.end('date')

            # we need to check that anything following the parsed
            # date is a time expression because it is often picked
            # up as a valid year if the hour is 2 digits
            fTime = False
            mm = ptc.CRE_TIMEHMS2.search(s)
            # "February 24th 1PM" doesn't get caught
            # "February 24th 12PM" does
            mYear = m.group('year')
            if mm is not None and mYear is not None:
                fTime = True
            else:
                # "February 24th 12:00"
                mm = ptc.CRE_TIMEHMS.search(s)
                if mm is not None and mYear is None:
                    fTime = True
            if fTime:
                hoursStart = mm.start('hours')

                if hoursStart < m.end('year'):
                    mEnd = hoursStart

            parseStr = s[mStart:mEnd]
            chunk1 = s[:mStart]
            chunk2 = s[mEnd:]

            s = '%s %s' % (chunk1, chunk2)
        else:
            parseStr = s
            s = ''

    if parseStr:
        debug and logging.debug(
            'found (date3) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyDateStr(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)


def _matchDateStd(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_DATE, used by L{Calendar.parse()}.
    Renamed from _partialParseDateStd for clarity.
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # Standard date format
    m = ptc.CRE_DATE.search(s)
    if m is not None:

        if (m.group('date') != s):
            # capture remaining string
            parseStr = m.group('date')
            chunk1 = s[:m.start('date')]
            chunk2 = s[m.end('date'):]
            s = '%s %s' % (chunk1, chunk2)
        else:
            parseStr = s
            s = ''

    if parseStr:
        debug and logging.debug(
            'found (date) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyDateStd(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)
