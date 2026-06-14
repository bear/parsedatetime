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

"""parsedatetime.parsing.days — day and weekday parsing

Contains:
- _matchDayStr / _applyDayStr  — natural language day strings (today, tomorrow, etc.)
- _matchWeekday / _applyWeekday — weekday name matching
- _CalculateDOWDelta            — day-of-week delta calculation
"""

from __future__ import with_statement, absolute_import, unicode_literals

import time
import logging
import datetime

from ..context import pdtContext

debug = False


def _CalculateDOWDelta(wd, wkdy, offset, style, currentDayStyle):
    """
    Based on the C{style} and C{currentDayStyle} determine what
    day-of-week value is to be returned.

    @type  wd:              integer
    @param wd:              day-of-week value for the current day
    @type  wkdy:            integer
    @param wkdy:            day-of-week value for the parsed day
    @type  offset:          integer
    @param offset:          offset direction for any modifiers (-1, 0, 1)
    @type  style:           integer
    @param style:           normally the value
                            set in C{Constants.DOWParseStyle}
    @type  currentDayStyle: integer
    @param currentDayStyle: normally the value
                            set in C{Constants.CurrentDOWParseStyle}

    @rtype:  integer
    @return: calculated day-of-week
    """
    diffBase = wkdy - wd
    origOffset = offset

    if offset == 2:
        # no modifier is present.
        # i.e. string to be parsed is just DOW
        if wkdy * style > wd * style or \
                currentDayStyle and wkdy == wd:
            # wkdy located in current week
            offset = 0
        elif style in (-1, 1):
            # wkdy located in last (-1) or next (1) week
            offset = style
        else:
            # invalid style, or should raise error?
            offset = 0

    # offset = -1 means last week
    # offset = 0 means current week
    # offset = 1 means next week
    diff = diffBase + 7 * offset
    if style == 1 and diff < -7:
        diff += 7
    elif style == -1 and diff > 7:
        diff -= 7

    debug and logging.debug(f'wd {wd}, wkdy {wkdy}, offset {origOffset}, style {style}, currentDayStyle {currentDayStyle}')

    return diff


def _applyDayStr(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchDayStr()}.
    Renamed from _evalDayStr for clarity.

    @type  calendar:      Calendar
    @param calendar:      Calendar instance
    @type  datetimeString: string
    @param datetimeString: text to evaluate
    @type  sourceTime:     struct_time
    @param sourceTime:     C{struct_time} value to use as the base

    @rtype:  struct_time
    @return: calculated C{struct_time} value
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

    # Given string is a natural language date string like today, tomorrow..
    (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

    try:
        offset = ptc.dayOffsets[s]
    except KeyError:
        offset = 0

    if ptc.StartTimeFromSourceTime:
        startHour = hr
        startMinute = mn
        startSecond = sec
    else:
        startHour = ptc.StartHour
        startMinute = 0
        startSecond = 0

    calendar.currentContext.updateAccuracy(pdtContext.ACU_DAY)
    start = datetime.datetime(yr, mth, dy, startHour,
                              startMinute, startSecond)
    target = start + datetime.timedelta(days=offset)
    return target.timetuple()


def _applyWeekday(calendar, datetimeString, sourceTime):
    """
    Evaluate text passed by L{_matchWeekday()}.
    Renamed from _evalWeekday for clarity.

    @type  calendar:      Calendar
    @param calendar:      Calendar instance
    @type  datetimeString: string
    @param datetimeString: text to evaluate
    @type  sourceTime:     struct_time
    @param sourceTime:     C{struct_time} value to use as the base

    @rtype:  struct_time
    @return: calculated C{struct_time} value
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

    # Given string is a weekday
    yr, mth, dy, hr, mn, sec, wd, yd, isdst = sourceTime

    start = datetime.datetime(yr, mth, dy, hr, mn, sec)
    wkdy = ptc.WeekdayOffsets[s]

    if wkdy > wd:
        qty = _CalculateDOWDelta(wd, wkdy, 2,
                                 ptc.DOWParseStyle,
                                 ptc.CurrentDOWParseStyle)
    else:
        qty = _CalculateDOWDelta(wd, wkdy, 2,
                                 ptc.DOWParseStyle,
                                 ptc.CurrentDOWParseStyle)

    calendar.currentContext.updateAccuracy(pdtContext.ACU_DAY)
    target = start + datetime.timedelta(days=qty)
    return target.timetuple()


def _matchDayStr(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_DAY, used by L{Calendar.parse()}.
    Renamed from _partialParseDayStr for clarity.

    @type  calendar:   Calendar
    @param calendar:   Calendar instance
    @type  s:          string
    @param s:          date/time text to evaluate
    @type  sourceTime: struct_time
    @param sourceTime: C{struct_time} value to use as the base

    @rtype:  tuple
    @return: tuple of remained date/time text, datetime object and
             an boolean value to describe if matched or not
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    # Natural language day strings
    m = ptc.CRE_DAY.search(s)
    if m is not None:

        if (m.group() != s):
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
            'found (day) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyDayStr(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)


def _matchWeekday(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_WEEKDAY, used by L{Calendar.parse()}.
    Renamed from _partialParseWeekday for clarity.

    @type  calendar:   Calendar
    @param calendar:   Calendar instance
    @type  s:          string
    @param s:          date/time text to evaluate
    @type  sourceTime: struct_time
    @param sourceTime: C{struct_time} value to use as the base

    @rtype:  tuple
    @return: tuple of remained date/time text, datetime object and
             an boolean value to describe if matched or not
    """
    ptc = calendar.ptc
    parseStr = None
    chunk1 = chunk2 = ''

    ctx = calendar.currentContext
    logging.debug(f'eval {s} with context - {ctx.hasDate}, {ctx.hasTime}')

    # Weekday
    m = ptc.CRE_WEEKDAY.search(s)
    if m is not None:
        gv = m.group()
        if s not in ptc.dayOffsets:

            if (gv != s):
                # capture remaining string
                parseStr = gv
                chunk1 = s[:m.start()]
                chunk2 = s[m.end():]
                s = '%s %s' % (chunk1, chunk2)
            else:
                parseStr = s
                s = ''

    if parseStr and not ctx.hasDate:
        debug and logging.debug(
            'found (weekday) [%s][%s][%s]', parseStr, chunk1, chunk2)
        sourceTime = _applyWeekday(calendar, parseStr, sourceTime)

    return s, sourceTime, bool(parseStr)
