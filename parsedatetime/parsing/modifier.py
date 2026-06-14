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

"""parsedatetime.parsing.modifier — modifier parsing (THE BEAST)

Contains:
- _matchModifier / _applyModifier — next/prev/from/after/prior/etc.

The _applyModifier function is the most complex parsing strategy,
handling modifiers applied to units, weekdays, and other date/time elements.
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging
import datetime

from ..context import pdtContext
from ..time_utils import _parse_date_rfc822, _parse_date_w3dtf, inc as _inc
from ..parsing.days import _CalculateDOWDelta

debug = False

VERSION_FLAG_STYLE = 1
VERSION_CONTEXT_STYLE = 2


def _applyModifier(calendar, modifier, chunk1, chunk2, sourceTime):
    """
    Evaluate the C{modifier} string and following text (passed in
    as C{chunk1} and C{chunk2}) and if they match any known modifiers
    calculate the delta and apply it to C{sourceTime}.
    Renamed from _evalModifier for clarity.

    @type  calendar:   Calendar
    @param calendar:   Calendar instance
    @type  modifier:   string
    @param modifier:   modifier text to apply to sourceTime
    @type  chunk1:     string
    @param chunk1:     text chunk that preceded modifier (if any)
    @type  chunk2:     string
    @param chunk2:     text chunk that followed modifier (if any)
    @type  sourceTime: struct_time
    @param sourceTime: C{struct_time} value to use as the base

    @rtype:  tuple
    @return: tuple of: remaining text and the modified sourceTime
    """
    ptc = calendar.ptc
    ctx = calendar.currentContext
    offset = ptc.Modifiers[modifier]

    if sourceTime is not None:
        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime
    else:
        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()

    if ptc.StartTimeFromSourceTime:
        startHour = hr
        startMinute = mn
        startSecond = sec
    else:
        startHour = ptc.StartHour
        startMinute = 0
        startSecond = 0

    # capture the units after the modifier and the remaining
    # string after the unit
    m = ptc.CRE_REMAINING.search(chunk2)
    if m is not None:
        index = m.start() + 1
        unit = chunk2[:m.start()]
        chunk2 = chunk2[index:]
    else:
        unit = chunk2
        chunk2 = ''

    debug and logging.debug(f'modifier [{modifier}] chunk1 [{chunk1}] chunk2 [{chunk2}] unit [{unit}]')

    if unit in ptc.units['months']:
        currentDaysInMonth = ptc.daysInMonth(mth, yr)
        if offset == 0:
            dy = currentDaysInMonth
            sourceTime = (yr, mth, dy, startHour, startMinute,
                          startSecond, wd, yd, isdst)
        elif offset == 2:
            # if day is the last day of the month, calculate the last day
            # of the next month
            if dy == currentDaysInMonth:
                dy = ptc.daysInMonth(mth + 1, yr)

            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = calendar.inc(start, month=1)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, 1, startHour,
                                      startMinute, startSecond)
            target = calendar.inc(start, month=offset)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_MONTH)

    elif unit in ptc.units['weeks']:
        if offset == 0:
            start = datetime.datetime(yr, mth, dy, 17, 0, 0)
            target = start + datetime.timedelta(days=(4 - wd))
            sourceTime = target.timetuple()
        elif offset == 2:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + datetime.timedelta(days=7)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + offset * datetime.timedelta(weeks=1)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_WEEK)

    elif unit in ptc.units['days']:
        if offset == 0:
            sourceTime = (yr, mth, dy, 17, 0, 0, wd, yd, isdst)
            ctx.updateAccuracy(ctx.ACU_HALFDAY)
        elif offset == 2:
            start = datetime.datetime(yr, mth, dy, hr, mn, sec)
            target = start + datetime.timedelta(days=1)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + datetime.timedelta(days=offset)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_DAY)

    elif unit in ptc.units['hours']:
        if offset == 0:
            sourceTime = (yr, mth, dy, hr, 0, 0, wd, yd, isdst)
        else:
            start = datetime.datetime(yr, mth, dy, hr, 0, 0)
            target = start + datetime.timedelta(hours=offset)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_HOUR)

    elif unit in ptc.units['years']:
        if offset == 0:
            sourceTime = (yr, 12, 31, hr, mn, sec, wd, yd, isdst)
        elif offset == 2:
            sourceTime = (yr + 1, mth, dy, hr, mn, sec, wd, yd, isdst)
        else:
            sourceTime = (yr + offset, 1, 1, startHour, startMinute,
                          startSecond, wd, yd, isdst)
        ctx.updateAccuracy(ctx.ACU_YEAR)

    elif modifier == 'eom':
        dy = ptc.daysInMonth(mth, yr)
        sourceTime = (yr, mth, dy, startHour, startMinute,
                      startSecond, wd, yd, isdst)
        ctx.updateAccuracy(ctx.ACU_DAY)

    elif modifier == 'eoy':
        mth = 12
        dy = ptc.daysInMonth(mth, yr)
        sourceTime = (yr, mth, dy, startHour, startMinute,
                      startSecond, wd, yd, isdst)
        ctx.updateAccuracy(ctx.ACU_MONTH)

    elif ptc.CRE_WEEKDAY.match(unit):
        m = ptc.CRE_WEEKDAY.match(unit)
        debug and logging.debug('CRE_WEEKDAY matched')
        wkdy = m.group()

        if modifier == 'eod':
            ctx.updateAccuracy(ctx.ACU_HOUR)
            # Calculate the upcoming weekday
            sourceTime, subctx = calendar.parse(wkdy, sourceTime,
                                                VERSION_CONTEXT_STYLE)
            sTime = ptc.getSource(modifier, sourceTime)
            if sTime is not None:
                sourceTime = sTime
                ctx.updateAccuracy(ctx.ACU_HALFDAY)
        else:
            # unless one of these modifiers is being applied to the
            # day-of-week, we want to start with target as the day
            # in the current week.
            dowOffset = offset
            relativeModifier = modifier not in ['this', 'next', 'last', 'prior', 'previous']
            if relativeModifier:
                dowOffset = 0

            wkdy = ptc.WeekdayOffsets[wkdy]
            diff = _CalculateDOWDelta(
                wd, wkdy, dowOffset, ptc.DOWParseStyle,
                ptc.CurrentDOWParseStyle)
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + datetime.timedelta(days=diff)

            if chunk1 != '' and relativeModifier:
                # consider "one day before thursday": we need to parse chunk1 ("one day")
                # and apply according to the offset ("before"), rather than allowing the
                # remaining parse step to apply "one day" without the offset direction.
                t, subctx = calendar.parse(chunk1, sourceTime, VERSION_CONTEXT_STYLE)
                if subctx.hasDateOrTime:
                    delta = time.mktime(t) - time.mktime(sourceTime)
                    target = start + datetime.timedelta(days=diff) + datetime.timedelta(seconds=delta * offset)
                    chunk1 = ''

            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_DAY)

    elif chunk1 == '' and chunk2 == '' and ptc.CRE_TIME.match(unit):
        m = ptc.CRE_TIME.match(unit)
        debug and logging.debug('CRE_TIME matched')
        (yr, mth, dy, hr, mn, sec, wd, yd, isdst), subctx = \
            calendar.parse(unit, sourceTime, VERSION_CONTEXT_STYLE)

        start = datetime.datetime(yr, mth, dy, hr, mn, sec)
        target = start + datetime.timedelta(days=offset)
        sourceTime = target.timetuple()
    elif unit.isdigit() and chunk2 in ptc.units['days']:
        offsetByUnit = int(unit)
        if offset == 0 and offsetByUnit == 0:
            sourceTime = (yr, mth, dy, 17, 0, 0, wd, yd, isdst)
            ctx.updateAccuracy(ctx.ACU_HALFDAY)
        elif offset == 2:
            start = datetime.datetime(yr, mth, dy, hr, mn, sec)
            target = start + datetime.timedelta(days=offsetByUnit)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + datetime.timedelta(days=offset * offsetByUnit)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_DAY)

    elif unit.isdigit() and chunk2 in ptc.units['weeks']:
        offsetByUnit = int(unit)
        if offset == 0:
            start = datetime.datetime(yr, mth, dy, 17, 0, 0)
            target = start + datetime.timedelta(days=(4 - wd))
            sourceTime = target.timetuple()
        elif offset == 2:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + datetime.timedelta(days=7 + offsetByUnit)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = start + offset * datetime.timedelta(weeks=1 + offsetByUnit)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_WEEK)

    elif unit.isdigit() and chunk2 in ptc.units['months']:
        offsetByUnit = int(unit)
        currentDaysInMonth = ptc.daysInMonth(mth, yr)
        if offset == 0:
            dy = currentDaysInMonth
            sourceTime = (yr, mth, dy, startHour, startMinute,
                          startSecond, wd, yd, isdst)
        elif offset == 2:
            # if day is the last day of the month, calculate the last day
            # of the next month
            if dy == currentDaysInMonth:
                dy = ptc.daysInMonth(mth + 1, yr)

            start = datetime.datetime(yr, mth, dy, startHour,
                                      startMinute, startSecond)
            target = calendar.inc(start, month=1)
            sourceTime = target.timetuple()
        else:
            start = datetime.datetime(yr, mth, 1, startHour,
                                      startMinute, startSecond)
            target = calendar.inc(start, month=offset * offsetByUnit)
            sourceTime = target.timetuple()
        ctx.updateAccuracy(ctx.ACU_MONTH)

    else:
        # check if the remaining text is parsable and if so,
        # use it as the base time for the modifier source time

        debug and logging.debug(f'check for modifications to source time [{chunk1}] [{unit}]')

        unit = unit.strip()
        if unit:
            s = '%s %s' % (unit, chunk2)
            t, subctx = calendar.parse(s, sourceTime, VERSION_CONTEXT_STYLE)

            if subctx.hasDate:  # working with dates
                u = unit.lower()
                if u in ptc.Months or \
                        u in ptc.shortMonths:
                    yr, mth, dy, hr, mn, sec, wd, yd, isdst = t
                    start = datetime.datetime(
                        yr, mth, dy, hr, mn, sec)
                    t = calendar.inc(start, year=offset).timetuple()
                elif u in ptc.Weekdays:
                    t = t + datetime.timedelta(weeks=offset)

            if subctx.hasDateOrTime:
                sourceTime = t
                chunk2 = ''

        chunk1 = chunk1.strip()

        # if the word after next is a number, the string is more than
        # likely to be "next 4 hrs" which we will have to combine the
        # units with the rest of the string
        if chunk1:
            try:
                m = list(ptc.CRE_NUMBER.finditer(chunk1))[-1]
            except IndexError:
                pass
            else:
                qty = None
                debug and logging.debug('CRE_NUMBER matched')
                qty = calendar._quantityToReal(m.group()) * offset
                chunk1 = '%s%s%s' % (chunk1[:m.start()],
                                     qty, chunk1[m.end():])
            t, subctx = calendar.parse(chunk1, sourceTime,
                                       VERSION_CONTEXT_STYLE)

            chunk1 = ''

            if subctx.hasDateOrTime:
                sourceTime = t

        debug and logging.debug(f'looking for modifier {modifier}')
        sTime = ptc.getSource(modifier, sourceTime)
        if sTime is not None:
            debug and logging.debug('modifier found in sources')
            sourceTime = sTime
            ctx.updateAccuracy(ctx.ACU_HALFDAY)

    debug and logging.debug(f'returning chunk = "{chunk1} {chunk2}" and sourceTime = {sourceTime}')

    return '%s %s' % (chunk1, chunk2), sourceTime


def _matchModifier(calendar, s, sourceTime):
    """
    Test if C{s} matched CRE_MODIFIER, used by L{Calendar.parse()}.
    Renamed from _partialParseModifier for clarity.

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

    # Modifier like next/prev/from/after/prior..
    m = ptc.CRE_MODIFIER.search(s)
    if m is not None:
        if m.group() != s:
            # capture remaining string
            parseStr = m.group()
            chunk1 = s[:m.start()].strip()
            chunk2 = s[m.end():].strip()
        else:
            parseStr = s

    if parseStr:
        debug and logging.debug(f'found (modifier) [{parseStr}][{chunk1}][{chunk2}]')
        s, sourceTime = _applyModifier(calendar, parseStr, chunk1,
                                       chunk2, sourceTime)

    return s, sourceTime, bool(parseStr)
