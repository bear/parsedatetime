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

"""parsedatetime/time_utils.py

Time-related utility functions extracted from the original monolith.

Includes feedparser-derived date/time extraction helpers, _buildTime,
inc(), and _pop_time_accuracy.
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging
import datetime
import email.utils

from .context import pdtContext

debug = False


# ─── Feedparser-derived helpers ──────────────────────────────────────────────

# Copied from feedparser.py
# Universal Feedparser
# Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Originally a def inside of _parse_date_w3dtf()
def _extract_date(m):
    year = int(m.group('year'))
    if year < 100:
        year = 100 * int(time.gmtime()[0] / 100) + int(year)
    if year < 1000:
        return 0, 0, 0
    julian = m.group('julian')
    if julian:
        julian = int(julian)
        month = julian / 30 + 1
        day = julian % 30 + 1
        jday = None
        while jday != julian:
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
            jday = time.gmtime(t)[-2]
            diff = abs(jday - julian)
            if jday > julian:
                if diff < day:
                    day = day - diff
                else:
                    month = month - 1
                    day = 31
            elif jday < julian:
                if day + diff < 28:
                    day = day + diff
                else:
                    month = month + 1
        return year, month, day
    month = m.group('month')
    day = 1
    if month is None:
        month = 1
    else:
        month = int(month)
        day = m.group('day')
        if day:
            day = int(day)
        else:
            day = 1
    return year, month, day


# Copied from feedparser.py
# Universal Feedparser
# Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Originally a def inside of _parse_date_w3dtf()
def _extract_time(m):
    if not m:
        return 0, 0, 0
    hours = m.group('hours')
    if not hours:
        return 0, 0, 0
    hours = int(hours)
    minutes = int(m.group('minutes'))
    seconds = m.group('seconds')
    if seconds:
        seconds = seconds.replace(',', '.').split('.', 1)[0]
        seconds = int(seconds)
    else:
        seconds = 0
    return hours, minutes, seconds


def _pop_time_accuracy(m, ctx):
    """Update context accuracy based on time regex match groups."""
    if not m:
        return
    if m.group('hours'):
        ctx.updateAccuracy(ctx.ACU_HOUR)
    if m.group('minutes'):
        ctx.updateAccuracy(ctx.ACU_MIN)
    if m.group('seconds'):
        ctx.updateAccuracy(ctx.ACU_SEC)


# ─── W3CDTF / RFC822 date parsing ────────────────────────────────────────────

_monthnames = set([
    'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
    'aug', 'sep', 'oct', 'nov', 'dec',
    'january', 'february', 'march', 'april', 'may', 'june', 'july',
    'august', 'september', 'october', 'november', 'december'])
_daynames = set(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])


# Copied from feedparser.py
# Universal Feedparser
# Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Modified to return a tuple instead of mktime
#
# Original comment:
#   W3DTF-style date parsing adapted from PyXML xml.utils.iso8601, written by
#   Drake and licensed under the Python license.  Removed all range checking
#   for month, day, hour, minute, and second, since mktime will normalize
#   these later
def __closure_parse_date_w3dtf():
    # the __extract_date and __extract_time methods were
    # copied-out so they could be used by my code --bear
    def __extract_tzd(m):
        '''Return the Time Zone Designator as an offset in seconds from UTC.'''
        if not m:
            return 0
        tzd = m.group('tzd')
        if not tzd:
            return 0
        if tzd == 'Z':
            return 0
        hours = int(m.group('tzdhours'))
        minutes = m.group('tzdminutes')
        if minutes:
            minutes = int(minutes)
        else:
            minutes = 0
        offset = (hours * 60 + minutes) * 60
        if tzd[0] == '+':
            return -offset
        return offset

    def _parse_date_w3dtf(dateString):
        m = __datetime_rx.match(dateString)
        if m is None or m.group() != dateString:
            return
        return _extract_date(m) + _extract_time(m) + (0, 0, 0)

    __date_re = (r'(?P<year>\d\d\d\d)'
                 r'(?:(?P<dsep>-|)'
                 r'(?:(?P<julian>\d\d\d)'
                 r'|(?P<month>\d\d)(?:(?P=dsep)(?P<day>\d\d))?))?')
    __tzd_re = r'(?P<tzd>[-+](?P<tzdhours>\d\d)(?::?(?P<tzdminutes>\d\d))|Z)'
    # __tzd_rx = re.compile(__tzd_re)
    __time_re = (r'(?P<hours>\d\d)(?P<tsep>:|)(?P<minutes>\d\d)'
                 r'(?:(?P=tsep)(?P<seconds>\d\d(?:[.,]\d+)?))?' + __tzd_re)
    __datetime_re = '%s(?:T%s)?' % (__date_re, __time_re)
    __datetime_rx = re.compile(__datetime_re)

    return _parse_date_w3dtf


_parse_date_w3dtf = __closure_parse_date_w3dtf()
del __closure_parse_date_w3dtf


# Copied from feedparser.py
# Universal Feedparser
# Copyright (c) 2002-2006, Mark Pilgrim, All rights reserved.
# Modified to return a tuple instead of mktime
def _parse_date_rfc822(dateString):
    '''Parse an RFC822, RFC1123, RFC2822, or asctime-style date'''
    data = dateString.split()
    if data[0][-1] in (',', '.') or data[0].lower() in _daynames:
        del data[0]
    if len(data) == 4:
        s = data[3]
        s = s.split('+', 1)
        if len(s) == 2:
            data[3:] = s
        else:
            data.append('')
        dateString = " ".join(data)
    if len(data) < 5:
        dateString += ' 00:00:00 GMT'
    return email.utils.parsedate_tz(dateString)


# ─── _buildTime ──────────────────────────────────────────────────────────────

def _buildTime(calendar, source, quantity, modifier, units):
    """
    Take C{quantity}, C{modifier} and C{unit} strings and convert them
    into values. After converting, calculate the time and return the
    adjusted sourceTime.

    @type  calendar:  Calendar
    @param calendar:  Calendar instance (for _quantityToReal, inc)
    @type  source:    time
    @param source:    time to use as the base (or source)
    @type  quantity:  string
    @param quantity:  quantity string
    @type  modifier:  string
    @param modifier:  how quantity and units modify the source time
    @type  units:     string
    @param units:     unit of the quantity (i.e. hours, days, months, etc)

    @rtype:  struct_time
    @return: C{struct_time} of the calculated time
    """
    ptc = calendar.ptc
    ctx = calendar.currentContext
    debug and logging.debug(f'_buildTime: [{quantity}][{modifier}][{units}]')

    if source is None:
        source = time.localtime()

    if quantity is None:
        quantity = ''
    else:
        quantity = quantity.strip()

    qty = calendar._quantityToReal(quantity)

    if modifier in ptc.Modifiers:
        qty = qty * ptc.Modifiers[modifier]

        if units is None or units == '':
            units = 'dy'

    # plurals are handled by regex's (could be a bug tho)

    (yr, mth, dy, hr, mn, sec, _, _, _) = source

    start = datetime.datetime(yr, mth, dy, hr, mn, sec)
    target = start
    realunit = units
    for key, values in ptc.units.items():
        if units in values:
            realunit = key
            break

    debug and logging.debug(f'units {units} --> realunit {realunit} (qty={qty})')

    try:
        if realunit in ('years', 'months'):
            target = inc(start, ptc, **{realunit[:-1]: qty})
        elif realunit in ('days', 'hours', 'minutes', 'seconds', 'weeks'):
            delta = datetime.timedelta(**{realunit: qty})
            target = start + delta
    except OverflowError:
        # OverflowError is raise when target.year larger than 9999
        pass
    else:
        ctx.updateAccuracy(realunit)

    return target.timetuple()


# ─── inc ─────────────────────────────────────────────────────────────────────

def inc(source, ptc, month=None, year=None):
    """
    Takes the given C{source} date, or current date if none is
    passed, and increments it according to the values passed in
    by month and/or year.

    This routine is needed because Python's C{timedelta()} function
    does not allow for month or year increments.

    @type  source: struct_time
    @param source: C{struct_time} value to increment
    @type  ptc:    Constants
    @param ptc:    Constants instance (for daysInMonth)
    @type  month:  float or integer
    @param month:  optional number of months to increment
    @type  year:   float or integer
    @param year:   optional number of years to increment

    @rtype:  datetime
    @return: C{source} incremented by the number of months and/or years
    """
    yr = source.year
    mth = source.month
    dy = source.day

    try:
        month = float(month)
    except (TypeError, ValueError):
        month = 0

    try:
        year = float(year)
    except (TypeError, ValueError):
        year = 0
    finally:
        month += year * 12
        year = 0

    subMi = 0.0
    maxDay = 0
    if month:
        mi = int(month)
        subMi = month - mi

        y = int(mi / 12.0)
        m = mi - y * 12

        mth = mth + m
        if mth < 1:  # cross start-of-year?
            y -= 1  # yes - decrement year
            mth += 12  # and fix month
        elif mth > 12:  # cross end-of-year?
            y += 1  # yes - increment year
            mth -= 12  # and fix month

        yr += y

        # if the day ends up past the last day of
        # the new month, set it to the last day
        maxDay = ptc.daysInMonth(mth, yr)
        if dy > maxDay:
            dy = maxDay

    if yr > datetime.MAXYEAR or yr < datetime.MINYEAR:
        raise OverflowError('year is out of range')

    d = source.replace(year=yr, month=mth, day=dy)
    if subMi:
        d += datetime.timedelta(days=subMi * maxDay)
    return source + (d - source)
