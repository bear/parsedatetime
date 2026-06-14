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

"""parsedatetime.parsing.ranges — date/time range parsing

Contains:
- evalRanges — evaluate date/time range strings
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging

debug = False

VERSION_FLAG_STYLE = 1
VERSION_CONTEXT_STYLE = 2


def evalRanges(calendar, datetimeString, sourceTime=None):
    """
    Evaluate the C{datetimeString} text and determine if
    it represents a date or time range.

    @type  calendar:      Calendar
    @param calendar:      Calendar instance
    @type  datetimeString: string
    @param datetimeString: datetime text to evaluate
    @type  sourceTime:     struct_time
    @param sourceTime:     C{struct_time} value to use as the base

    @rtype:  tuple
    @return: tuple of: start datetime, end datetime and the invalid flag
    """
    ptc = calendar.ptc
    rangeFlag = retFlag = 0
    startStr = endStr = ''

    s = datetimeString.strip().lower()

    if ptc.rangeSep in s:
        s = s.replace(ptc.rangeSep, ' %s ' % ptc.rangeSep)
        s = s.replace('  ', ' ')

    for cre, rflag in [(ptc.CRE_TIMERNG1, 1),
                       (ptc.CRE_TIMERNG2, 2),
                       (ptc.CRE_TIMERNG4, 7),
                       (ptc.CRE_TIMERNG3, 3),
                       (ptc.CRE_DATERNG1, 4),
                       (ptc.CRE_DATERNG2, 5),
                       (ptc.CRE_DATERNG3, 6)]:
        m = cre.search(s)
        if m is not None:
            rangeFlag = rflag
            break

    debug and logging.debug(f'evalRanges: rangeFlag = {rangeFlag} [{s}]')

    if m is not None:
        if (m.group() != s):
            # capture remaining string
            parseStr = m.group()
            chunk1 = s[:m.start()]
            chunk2 = s[m.end():]
            s = '%s %s' % (chunk1, chunk2)

            sourceTime, ctx = calendar.parse(s, sourceTime,
                                             VERSION_CONTEXT_STYLE)

            if not ctx.hasDateOrTime:
                sourceTime = None
        else:
            parseStr = s

    if rangeFlag in (1, 2):
        m = re.search(ptc.rangeSep, parseStr)
        startStr = parseStr[:m.start()]
        endStr = parseStr[m.start() + 1:]
        retFlag = 2

    elif rangeFlag in (3, 7):
        m = re.search(ptc.rangeSep, parseStr)
        # capturing the meridian from the end time
        if ptc.usesMeridian:
            ampm = re.search(ptc.am[0], parseStr)

            # appending the meridian to the start time
            if ampm is not None:
                startStr = parseStr[:m.start()] + ptc.meridian[0]
            else:
                startStr = parseStr[:m.start()] + ptc.meridian[1]
        else:
            startStr = parseStr[:m.start()]

        endStr = parseStr[m.start() + 1:]
        retFlag = 2

    elif rangeFlag == 4:
        m = re.search(ptc.rangeSep, parseStr)
        startStr = parseStr[:m.start()]
        endStr = parseStr[m.start() + 1:]
        retFlag = 1

    elif rangeFlag == 5:
        m = re.search(ptc.rangeSep, parseStr)
        endStr = parseStr[m.start() + 1:]

        # capturing the year from the end date
        date = ptc.CRE_DATE3.search(endStr)
        endYear = date.group('year')

        # appending the year to the start date if the start date
        # does not have year information and the end date does.
        # eg : "Aug 21 - Sep 4, 2007"
        if endYear is not None:
            startStr = (parseStr[:m.start()]).strip()
            date = ptc.CRE_DATE3.search(startStr)
            startYear = date.group('year')

            if startYear is None:
                startStr = startStr + ', ' + endYear
        else:
            startStr = parseStr[:m.start()]

        retFlag = 1

    elif rangeFlag == 6:
        m = re.search(ptc.rangeSep, parseStr)

        startStr = parseStr[:m.start()]

        # capturing the month from the start date
        mth = ptc.CRE_DATE3.search(startStr)
        mth = mth.group('mthname')

        # appending the month name to the end date
        endStr = mth + parseStr[(m.start() + 1):]

        retFlag = 1

    else:
        # if range is not found
        startDT = endDT = time.localtime()

    if retFlag:
        startDT, sctx = calendar.parse(startStr, sourceTime,
                                       VERSION_CONTEXT_STYLE)
        endDT, ectx = calendar.parse(endStr, sourceTime,
                                     VERSION_CONTEXT_STYLE)

        if not sctx.hasDateOrTime or not ectx.hasDateOrTime:
            retFlag = 0

    return startDT, endDT, retFlag
