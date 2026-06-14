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

"""parsedatetime.calendar — slim Calendar orchestrator

The Calendar class delegates parsing to domain modules in parsedatetime.parsing
and utility functions in parsedatetime.time_utils.
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging
import warnings
import datetime
import calendar
import contextlib

from .pdt_locales import (locales as _locales,
                          get_icu, load_locale,
                          pdtLocales)
from .context import pdtContext, pdtContextStack
from .warns import pdt20DeprecationWarning
from .time_utils import (
    _extract_date, _extract_time, _pop_time_accuracy,
    _parse_date_w3dtf, _parse_date_rfc822,
    _buildTime, inc as _inc,
)
from .parsing.days import _matchDayStr, _applyDayStr, _matchWeekday, _applyWeekday, _CalculateDOWDelta
from .parsing.times import _matchTimeStr, _applyTimeStr, _matchMeridian, _applyMeridian, _matchTimeStd, _applyTimeStd
from .parsing.dates import _matchDateStr, _applyDateStr, _matchDateStd, _applyDateStd
from .parsing.units import _matchUnits, _applyUnits, _matchQUnits, _applyQUnits, _UnitsTrapped
from .parsing.modifier import _matchModifier, _applyModifier
from .parsing.ranges import evalRanges as _evalRanges
from .parsing.nlp import nlp as _nlp

VERSION_FLAG_STYLE = 1
VERSION_CONTEXT_STYLE = 2


class Calendar(object):

    """
    A collection of routines to input, parse and manipulate date and times.
    The text can either be 'normal' date values or it can be human readable.
    """

    def __init__(self, constants=None, version=VERSION_CONTEXT_STYLE):
        """
        Default constructor for the L{Calendar} class.

        @type  constants: object
        @param constants: Instance of the class L{Constants}
        @type  version:   integer
        @param version:   Default style version of current Calendar instance.
                          Valid value can be 1 (L{VERSION_FLAG_STYLE}) or
                          2 (L{VERSION_CONTEXT_STYLE}). See L{parse()}.

        @rtype:  object
        @return: L{Calendar} instance
        """
        # if a constants reference is not included, use default
        if constants is None:
            self.ptc = Constants()
        else:
            self.ptc = constants

        self.version = version
        if version == VERSION_FLAG_STYLE:
            warnings.warn(
                'Flag style will be deprecated in parsedatetime 2.0. '
                'Instead use the context style by instantiating `Calendar()` '
                'with argument `version=parsedatetime.VERSION_CONTEXT_STYLE`.',
                pdt20DeprecationWarning)
        self._ctxStack = pdtContextStack()

    @contextlib.contextmanager
    def context(self):
        ctx = pdtContext()
        self._ctxStack.push(ctx)
        yield ctx
        ctx = self._ctxStack.pop()
        if not self._ctxStack.isEmpty():
            self.currentContext.update(ctx)

    @property
    def currentContext(self):
        return self._ctxStack.last()

    def _convertUnitAsWords(self, unitText):
        """
        Converts text units into their number value.

        @type  unitText: string
        @param unitText: number text to convert

        @rtype:  integer
        @return: numerical value of unitText
        """
        word_list, a, b = re.split(r"[,\s-]+", unitText), 0, 0
        for word in word_list:
            x = self.ptc.small.get(word)
            if x is not None:
                a += x
            elif word == "hundred":
                a *= 100
            else:
                x = self.ptc.magnitude.get(word)
                if x is not None:
                    b += a * x
                    a = 0
                elif word in self.ptc.ignore:
                    pass
                else:
                    raise Exception("Unknown number: " + word)
        return a + b

    def _buildTime(self, source, quantity, modifier, units):
        """
        Take C{quantity}, C{modifier} and C{unit} strings and convert them
        into values. After converting, calculate the time and return the
        adjusted sourceTime.

        Delegates to L{time_utils._buildTime}.

        @type  source:   time
        @param source:   time to use as the base (or source)
        @type  quantity: string
        @param quantity: quantity string
        @type  modifier: string
        @param modifier: how quantity and units modify the source time
        @type  units:    string
        @param units:    unit of the quantity (i.e. hours, days, months, etc)

        @rtype:  struct_time
        @return: C{struct_time} of the calculated time
        """
        return _buildTime(self, source, quantity, modifier, units)

    def parseDate(self, dateString, sourceTime=None):
        """
        Parse short-form date strings::

            '05/28/2006' or '04.21'

        @type  dateString: string
        @param dateString: text to convert to a C{datetime}
        @type  sourceTime:     struct_time
        @param sourceTime:     C{struct_time} value to use as the base

        @rtype:  struct_time
        @return: calculated C{struct_time} value of dateString
        """
        if sourceTime is None:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()
        else:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = sourceTime

        # values pulled from regex's will be stored here and later
        # assigned to mth, dy, yr based on information from the locale
        # -1 is used as the marker value because we want zero values
        # to be passed thru so they can be flagged as errors later
        v1 = -1
        v2 = -1
        v3 = -1
        accuracy = []

        s = dateString
        m = self.ptc.CRE_DATE2.search(s)
        if m is not None:
            index = m.start()
            v1 = int(s[:index])
            s = s[index + 1:]

        m = self.ptc.CRE_DATE2.search(s)
        if m is not None:
            index = m.start()
            v2 = int(s[:index])
            v3 = int(s[index + 1:])
        else:
            v2 = int(s.strip())

        v = [v1, v2, v3]
        d = {'m': mth, 'd': dy, 'y': yr}

        # yyyy/mm/dd format
        dp_order = self.ptc.dp_order if v1 <= 31 else ['y', 'm', 'd']

        for i in range(0, 3):
            n = v[i]
            c = dp_order[i]
            if n >= 0:
                d[c] = n
                accuracy.append({'m': pdtContext.ACU_MONTH,
                                 'd': pdtContext.ACU_DAY,
                                 'y': pdtContext.ACU_YEAR}[c])

        # if the year is not specified and the date has already
        # passed, increment the year
        if v3 == -1 and ((mth > d['m']) or (mth == d['m'] and dy > d['d'])):
            yr = d['y'] + self.ptc.YearParseStyle
        else:
            yr = d['y']

        mth = d['m']
        dy = d['d']

        # birthday epoch constraint
        if yr < self.ptc.BirthdayEpoch:
            yr += 2000
        elif yr < 100:
            yr += 1900

        daysInCurrentMonth = self.ptc.daysInMonth(mth, yr)
        debug and logging.debug(f'parseDate: {yr} {mth} {dy} {daysInCurrentMonth}')

        with self.context() as ctx:
            if mth > 0 and mth <= 12 and dy > 0 and \
                    dy <= daysInCurrentMonth:
                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
                ctx.updateAccuracy(*accuracy)
            else:
                # return current time if date string is invalid
                sourceTime = time.localtime()

        return sourceTime

    def parseDateText(self, dateString, sourceTime=None):
        """
        Parse long-form date strings::

            'May 31st, 2006'
            'Jan 1st'
            'July 2006'

        @type  dateString: string
        @param dateString: text to convert to a datetime
        @type  sourceTime:     struct_time
        @param sourceTime:     C{struct_time} value to use as the base

        @rtype:  struct_time
        @return: calculated C{struct_time} value of dateString
        """
        if sourceTime is None:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = time.localtime()
        else:
            yr, mth, dy, hr, mn, sec, wd, yd, isdst = sourceTime

        currentMth = mth
        currentDy = dy
        accuracy = []

        debug and logging.debug(f'parseDateText currentMth {mth} currentDy {dy}')

        s = dateString.lower()
        m = self.ptc.CRE_DATE3.search(s)
        mth = m.group('mthname')
        mth = self.ptc.MonthOffsets[mth]
        accuracy.append('month')

        if m.group('day') is not None:
            dy = int(m.group('day'))
            accuracy.append('day')
        else:
            dy = 1

        if m.group('year') is not None:
            yr = int(m.group('year'))
            accuracy.append('year')

            # birthday epoch constraint
            if yr < self.ptc.BirthdayEpoch:
                yr += 2000
            elif yr < 100:
                yr += 1900

        elif (mth < currentMth) or (mth == currentMth and dy < currentDy):
            # if that day and month have already passed in this year,
            # then increment the year by 1
            yr += self.ptc.YearParseStyle

        with self.context() as ctx:
            if dy > 0 and dy <= self.ptc.daysInMonth(mth, yr):
                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)
                ctx.updateAccuracy(*accuracy)
            else:
                # Return current time if date string is invalid
                sourceTime = time.localtime()

        debug and logging.debug(f'parseDateText returned mth {mth} dy {dy} yr {yr} sourceTime {sourceTime}')

        return sourceTime

    def evalRanges(self, datetimeString, sourceTime=None):
        """
        Evaluate the C{datetimeString} text and determine if
        it represents a date or time range.

        Delegates to L{parsing.ranges.evalRanges}.

        @type  datetimeString: string
        @param datetimeString: datetime text to evaluate
        @type  sourceTime:     struct_time
        @param sourceTime:     C{struct_time} value to use as the base

        @rtype:  tuple
        @return: tuple of: start datetime, end datetime and the invalid flag
        """
        return _evalRanges(self, datetimeString, sourceTime)

    def _CalculateDOWDelta(self, wd, wkdy, offset, style, currentDayStyle):
        """
        Based on the C{style} and C{currentDayStyle} determine what
        day-of-week value is to be returned.

        Delegates to L{parsing.days._CalculateDOWDelta}.

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
        return _CalculateDOWDelta(wd, wkdy, offset, style, currentDayStyle)

    def _quantityToReal(self, quantity):
        """
        Convert a quantity, either spelled-out or numeric, to a float

        @type    quantity: string
        @param   quantity: quantity to parse to float
        @rtype:  int
        @return: the quantity as an float, defaulting to 0.0
        """
        if not quantity:
            return 1.0

        try:
            return float(quantity.replace(',', '.'))
        except ValueError:
            pass

        try:
            return float(self.ptc.numbers[quantity])
        except KeyError:
            pass

        return 0.0

    def _evalModifier(self, modifier, chunk1, chunk2, sourceTime):
        """
        Evaluate the C{modifier} string and following text.
        Delegates to L{parsing.modifier._applyModifier}.
        """
        return _applyModifier(self, modifier, chunk1, chunk2, sourceTime)

    def _evalDT(self, datetimeString, sourceTime):
        """
        Calculate the datetime from known format like RFC822 or W3CDTF

        Examples handled::
            RFC822, W3CDTF formatted dates
            HH:MM[:SS][ am/pm]
            MM/DD/YYYY
            DD MMMM YYYY

        @type  datetimeString: string
        @param datetimeString: text to try and parse as more "traditional"
                               date/time text
        @type  sourceTime:     struct_time
        @param sourceTime:     C{struct_time} value to use as the base

        @rtype:  datetime
        @return: calculated C{struct_time} value or current C{struct_time}
                 if not parsed
        """
        ctx = self.currentContext
        s = datetimeString.strip()

        # Given string date is a RFC822 date
        if sourceTime is None:
            sourceTime = _parse_date_rfc822(s)
            debug and logging.debug(
                'attempt to parse as rfc822 - %s', str(sourceTime))

            if sourceTime is not None:
                (yr, mth, dy, hr, mn, sec, wd, yd, isdst, _) = sourceTime
                ctx.updateAccuracy(ctx.ACU_YEAR, ctx.ACU_MONTH, ctx.ACU_DAY)

                if hr != 0 and mn != 0 and sec != 0:
                    ctx.updateAccuracy(ctx.ACU_HOUR, ctx.ACU_MIN, ctx.ACU_SEC)

                sourceTime = (yr, mth, dy, hr, mn, sec, wd, yd, isdst)

        # Given string date is a W3CDTF date
        if sourceTime is None:
            sourceTime = _parse_date_w3dtf(s)

            if sourceTime is not None:
                ctx.updateAccuracy(ctx.ACU_YEAR, ctx.ACU_MONTH, ctx.ACU_DAY,
                                   ctx.ACU_HOUR, ctx.ACU_MIN, ctx.ACU_SEC)

        if sourceTime is None:
            sourceTime = time.localtime()

        return sourceTime

    def _evalUnits(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseUnits()}.
        Delegates to L{parsing.units._applyUnits}.
        """
        return _applyUnits(self, datetimeString, sourceTime)

    def _evalQUnits(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseQUnits()}.
        Delegates to L{parsing.units._applyQUnits}.
        """
        return _applyQUnits(self, datetimeString, sourceTime)

    def _evalDateStr(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseDateStr()}.
        Delegates to L{parsing.dates._applyDateStr}.
        """
        return _applyDateStr(self, datetimeString, sourceTime)

    def _evalDateStd(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseDateStd()}.
        Delegates to L{parsing.dates._applyDateStd}.
        """
        return _applyDateStd(self, datetimeString, sourceTime)

    def _evalDayStr(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseDaystr()}.
        Delegates to L{parsing.days._applyDayStr}.
        """
        return _applyDayStr(self, datetimeString, sourceTime)

    def _evalWeekday(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseWeekday()}.
        Delegates to L{parsing.days._applyWeekday}.
        """
        return _applyWeekday(self, datetimeString, sourceTime)

    def _evalTimeStr(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseTimeStr()}.
        Delegates to L{parsing.times._applyTimeStr}.
        """
        return _applyTimeStr(self, datetimeString, sourceTime)

    def _evalMeridian(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseMeridian()}.
        Delegates to L{parsing.times._applyMeridian}.
        """
        return _applyMeridian(self, datetimeString, sourceTime)

    def _evalTimeStd(self, datetimeString, sourceTime):
        """
        Evaluate text passed by L{_partialParseTimeStd()}.
        Delegates to L{parsing.times._applyTimeStd}.
        """
        return _applyTimeStd(self, datetimeString, sourceTime)

    def _UnitsTrapped(self, s, m, key):
        """
        Check if a day suffix got trapped by a unit match.
        Delegates to L{parsing.units._UnitsTrapped}.
        """
        return _UnitsTrapped(self.ptc, s, m, key)

    def _partialParseModifier(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_MODIFIER, used by L{parse()}.
        Delegates to L{parsing.modifier._matchModifier}.
        """
        return _matchModifier(self, s, sourceTime)

    def _partialParseUnits(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_UNITS, used by L{parse()}.
        Delegates to L{parsing.units._matchUnits}.
        """
        return _matchUnits(self, s, sourceTime)

    def _partialParseQUnits(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_QUNITS, used by L{parse()}.
        Delegates to L{parsing.units._matchQUnits}.
        """
        return _matchQUnits(self, s, sourceTime)

    def _partialParseDateStr(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_DATE3, used by L{parse()}.
        Delegates to L{parsing.dates._matchDateStr}.
        """
        return _matchDateStr(self, s, sourceTime)

    def _partialParseDateStd(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_DATE, used by L{parse()}.
        Delegates to L{parsing.dates._matchDateStd}.
        """
        return _matchDateStd(self, s, sourceTime)

    def _partialParseDayStr(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_DAY, used by L{parse()}.
        Delegates to L{parsing.days._matchDayStr}.
        """
        return _matchDayStr(self, s, sourceTime)

    def _partialParseWeekday(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_WEEKDAY, used by L{parse()}.
        Delegates to L{parsing.days._matchWeekday}.
        """
        return _matchWeekday(self, s, sourceTime)

    def _partialParseTimeStr(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_TIME, used by L{parse()}.
        Delegates to L{parsing.times._matchTimeStr}.
        """
        return _matchTimeStr(self, s, sourceTime)

    def _partialParseMeridian(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_TIMEHMS2, used by L{parse()}.
        Delegates to L{parsing.times._matchMeridian}.
        """
        return _matchMeridian(self, s, sourceTime)

    def _partialParseTimeStd(self, s, sourceTime):
        """
        Test if giving C{s} matched CRE_TIMEHMS, used by L{parse()}.
        Delegates to L{parsing.times._matchTimeStd}.
        """
        return _matchTimeStd(self, s, sourceTime)

    def parseDT(self, datetimeString, sourceTime=None,
                tzinfo=None, version=None):
        """
        C{datetimeString} is as C{.parse}, C{sourceTime} has the same semantic
        meaning as C{.parse}, but now also accepts datetime objects.  C{tzinfo}
        accepts a tzinfo object.  It is advisable to use pytz.


        @type  datetimeString: string
        @param datetimeString: date/time text to evaluate
        @type  sourceTime:     struct_time, datetime, date, time
        @param sourceTime:     time value to use as the base
        @type  tzinfo:         tzinfo
        @param tzinfo:         Timezone to apply to generated datetime objs.
        @type  version:        integer
        @param version:        style version, default will use L{Calendar}
                               parameter version value

        @rtype:  tuple
        @return: tuple of: modified C{sourceTime} and the result flag/context

        see .parse for return code details.
        """
        # if sourceTime has a timetuple method, use thet, else, just pass the
        # entire thing to parse and prey the user knows what the hell they are
        # doing.
        sourceTime = getattr(sourceTime, 'timetuple', (lambda: sourceTime))()
        # You REALLY SHOULD be using pytz.  Using localize if available,
        # hacking if not.  Note, None is a valid tzinfo object in the case of
        # the ugly hack.
        localize = getattr(
            tzinfo,
            'localize',
            (lambda dt: dt.replace(tzinfo=tzinfo)),  # ugly hack is ugly :(
        )

        # Punt
        time_struct, ret_code = self.parse(
            datetimeString,
            sourceTime=sourceTime,
            version=version)

        # Comments from GHI indicate that it is desired to have the same return
        # signature on this method as that one it punts to, with the exception
        # of using datetime objects instead of time_structs.
        dt = localize(datetime.datetime(*time_struct[:6]))
        return dt, ret_code

    def parse(self, datetimeString, sourceTime=None, version=None):
        """
        Splits the given C{datetimeString} into tokens, finds the regex
        patterns that match and then calculates a C{struct_time} value from
        the chunks.

        If C{sourceTime} is given then the C{struct_time} value will be
        calculated from that value, otherwise from the current date/time.

        If the C{datetimeString} is parsed and date/time value found, then::

            If C{version} equals to L{VERSION_FLAG_STYLE}, the second item of
            the returned tuple will be a flag to let you know what kind of
            C{struct_time} value is being returned::

                0 = not parsed at all
                1 = parsed as a C{date}
                2 = parsed as a C{time}
                3 = parsed as a C{datetime}

            If C{version} equals to L{VERSION_CONTEXT_STYLE}, the second value
            will be an instance of L{pdtContext}

        @type  datetimeString: string
        @param datetimeString: date/time text to evaluate
        @type  sourceTime:     struct_time
        @param sourceTime:     C{struct_time} value to use as the base
        @type  version:        integer
        @param version:        style version, default will use L{Calendar}
                               parameter version value

        @rtype:  tuple
        @return: tuple of: modified C{sourceTime} and the result flag/context
        """
        debug and logging.debug('parse()')

        datetimeString = re.sub(r'(\w)\.(\s)', r'\1\2', datetimeString)
        datetimeString = re.sub(r'(\w)[\'"](\s|$)', r'\1 \2', datetimeString)
        datetimeString = re.sub(r'(\s|^)[\'"](\w)', r'\1 \2', datetimeString)

        if sourceTime:
            if isinstance(sourceTime, datetime.datetime):
                debug and logging.debug('coercing datetime to timetuple')
                sourceTime = sourceTime.timetuple()
            else:
                if not isinstance(sourceTime, time.struct_time) and \
                        not isinstance(sourceTime, tuple):
                    raise ValueError('sourceTime is not a struct_time')
        else:
            sourceTime = time.localtime()

        with self.context() as ctx:
            s = datetimeString.lower().strip()
            debug and logging.debug(f'remainedString (before parsing): [{s}]')

            while s:
                for parseMeth in (self._partialParseModifier,
                                  self._partialParseUnits,
                                  self._partialParseQUnits,
                                  self._partialParseDateStr,
                                  self._partialParseDateStd,
                                  self._partialParseDayStr,
                                  self._partialParseWeekday,
                                  self._partialParseTimeStr,
                                  self._partialParseMeridian,
                                  self._partialParseTimeStd):
                    retS, retTime, matched = parseMeth(s, sourceTime)
                    if matched:
                        s, sourceTime = retS.strip(), retTime
                        break
                else:
                    # nothing matched
                    s = ''

                debug and logging.debug(f'hasDate: [{ctx.hasDate}], hasTime: [{ctx.hasTime}]')
                debug and logging.debug(f'remainedString: [{s}]')

            # String is not parsed at all
            if sourceTime is None:
                debug and logging.debug(f'not parsed [{sourceTime}]')
                sourceTime = time.localtime()

        if not isinstance(sourceTime, time.struct_time):
            sourceTime = time.struct_time(sourceTime)

        version = self.version if version is None else version
        if version == VERSION_CONTEXT_STYLE:
            return sourceTime, ctx
        else:
            return sourceTime, ctx.dateTimeFlag

    def inc(self, source, month=None, year=None):
        """
        Takes the given C{source} date, or current date if none is
        passed, and increments it according to the values passed in
        by month and/or year.

        This routine is needed because Python's C{timedelta()} function
        does not allow for month or year increments.

        Delegates to L{time_utils.inc}.

        @type  source: struct_time
        @param source: C{struct_time} value to increment
        @type  month:  float or integer
        @param month:  optional number of months to increment
        @type  year:   float or integer
        @param year:   optional number of years to increment

        @rtype:  datetime
        @return: C{source} incremented by the number of months and/or years
        """
        return _inc(source, self.ptc, month=month, year=year)

    def nlp(self, inputString, sourceTime=None, version=None):
        """Utilizes parse() after making judgements about what datetime
        information belongs together.

        Delegates to L{parsing.nlp.nlp}.

        It makes logical groupings based on proximity and returns a parsed
        datetime for each matched grouping of datetime text, along with
        location info within the given inputString.

        @type  inputString: string
        @param inputString: natural language text to evaluate
        @type  sourceTime:  struct_time
        @param sourceTime:  C{struct_time} value to use as the base
        @type  version:     integer
        @param version:     style version, default will use L{Calendar}
                            parameter version value

        @rtype:  tuple or None
        @return: tuple of tuples in the format (parsed_datetime as
                 datetime.datetime, flags as int, start_pos as int,
                 end_pos as int, matched_text as string) or None if there
                 were no matches
        """
        return _nlp(self, inputString, sourceTime, version)

debug = False


# ─── _initSymbols ────────────────────────────────────────────────────────────

def _initSymbols(ptc):
    """
    Initialize symbols and single character constants.
    """
    # build am and pm lists to contain
    # original case, lowercase, first-char and dotted
    # versions of the meridian text
    ptc.am = ['', '']
    ptc.pm = ['', '']
    for idx, xm in enumerate(ptc.locale.meridian[:2]):
        # 0: am
        # 1: pm
        target = ['am', 'pm'][idx]
        setattr(ptc, target, [xm])
        target = getattr(ptc, target)
        if xm:
            lxm = xm.lower()
            target.extend((xm[0], '{0}.{1}.'.format(*xm),
                           lxm, lxm[0], '{0}.{1}.'.format(*lxm)))


# ─── Constants ───────────────────────────────────────────────────────────────

class Constants(object):

    """
    Default set of constants for parsedatetime.

    If PyICU is present, then the class will first try to get PyICU
    to return a locale specified by C{localeID}.  If either C{localeID} is
    None or if the locale does not exist within PyICU, then each of the
    locales defined in C{fallbackLocales} is tried in order.

    If PyICU is not present or none of the specified locales can be used,
    then the class will initialize itself to the en_US locale.

    if PyICU is not present or not requested, only the locales defined by
    C{pdtLocales} will be searched.
    """

    def __init__(self, localeID=None, usePyICU=True,
                 fallbackLocales=['en_US']):
        self.localeID = localeID
        self.fallbackLocales = fallbackLocales[:]

        if 'en_US' not in self.fallbackLocales:
            self.fallbackLocales.append('en_US')

        # define non-locale specific constants
        self.locale = None
        self.usePyICU = usePyICU

        # starting cache of leap years
        # daysInMonth will add to this if during
        # runtime it gets a request for a year not found
        self._leapYears = list(range(1904, 2097, 4))

        self.Second = 1
        self.Minute = 60  # 60 * self.Second
        self.Hour = 3600  # 60 * self.Minute
        self.Day = 86400  # 24 * self.Hour
        self.Week = 604800  # 7   * self.Day
        self.Month = 2592000  # 30  * self.Day
        self.Year = 31536000  # 365 * self.Day

        self._DaysInMonthList = (31, 28, 31, 30, 31, 30,
                                 31, 31, 30, 31, 30, 31)
        self.rangeSep = '-'
        self.BirthdayEpoch = 50

        # When True the starting time for all relative calculations will come
        # from the given SourceTime, otherwise it will be self.StartHour

        self.StartTimeFromSourceTime = False

        # The hour of the day that will be used as the starting time for all
        # relative calculations when self.StartTimeFromSourceTime is False

        self.StartHour = 9

        # YearParseStyle controls how we parse "Jun 12", i.e. dates that do
        # not have a year present.  The default is to compare the date given
        # to the current date, and if prior, then assume the next year.
        # Setting this to 0 will prevent that.

        self.YearParseStyle = 1

        # DOWParseStyle controls how we parse "Tuesday"

        self.DOWParseStyle = 1

        # CurrentDOWParseStyle controls how we parse "Friday"

        self.CurrentDOWParseStyle = False

        if self.usePyICU:
            self.locale = get_icu(self.localeID)

            if self.locale.icu is None:
                self.usePyICU = False
                self.locale = None

        if self.locale is None:
            if self.localeID not in pdtLocales:
                for localeId in range(0, len(self.fallbackLocales)):
                    self.localeID = self.fallbackLocales[localeId]
                    if self.localeID in pdtLocales:
                        break

            self.locale = pdtLocales[self.localeID]

        if self.locale is not None:
            # Delegate regex pattern building to the constants module
            from .constants import build_regex_patterns
            build_regex_patterns(self)

        _initSymbols(self)

    def __getattr__(self, name):
        if name in self.cre_keys:
            value = re.compile(self.cre_source[name], self.re_option)
            setattr(self, name, value)
            return value
        elif name in self.locale.locale_keys:
            return getattr(self.locale, name)
        else:
            raise AttributeError(name)

    def daysInMonth(self, month, year):
        """
        Take the given month (1-12) and a given year (4 digit) return
        the number of days in the month adjusting for leap year as needed
        """
        result = None
        debug and logging.debug(f'daysInMonth({month}, {year})')
        if month > 0 and month <= 12:
            result = self._DaysInMonthList[month - 1]

            if month == 2:
                if year in self._leapYears:
                    result += 1
                else:
                    if calendar.isleap(year):
                        self._leapYears.append(year)
                        result += 1

        return result

    def getSource(self, sourceKey, sourceTime=None):
        """
        GetReturn a date/time tuple based on the giving source key
        and the corresponding key found in self.re_sources.

        The current time is used as the default and any specified
        item found in self.re_sources is inserted into the value
        and the generated dictionary is returned.
        """
        if sourceKey not in self.re_sources:
            return None

        if sourceTime is None:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = time.localtime()
        else:
            (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = sourceTime

        defaults = {'yr': yr, 'mth': mth, 'dy': dy,
                    'hr': hr, 'mn': mn, 'sec': sec}

        source = self.re_sources[sourceKey]

        values = {}

        for key, default in defaults.items():
            values[key] = source.get(key, default)

        return (values['yr'], values['mth'], values['dy'],
                values['hr'], values['mn'], values['sec'],
                wd, yd, isdst)
