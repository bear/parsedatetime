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

"""parsedatetime.parsing.nlp — natural language processing for date/time

Contains:
- nlp — NLP-based date/time extraction from free text
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging
import datetime

from ..parsing.units import _UnitsTrapped

debug = False

VERSION_FLAG_STYLE = 1
VERSION_CONTEXT_STYLE = 2


def nlp(calendar, inputString, sourceTime=None, version=None):
    """Utilizes parse() after making judgements about what datetime
    information belongs together.

    It makes logical groupings based on proximity and returns a parsed
    datetime for each matched grouping of datetime text, along with
    location info within the given inputString.

    @type  calendar:    Calendar
    @param calendar:    Calendar instance
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
    ptc = calendar.ptc
    orig_inputstring = inputString

    # replace periods at the end of sentences w/ spaces
    # opposed to removing them altogether in order to
    # retain relative positions (identified by alpha, period, space).
    # this is required for some of the regex patterns to match
    inputString = re.sub(r'(\w)(\.)(\s)', r'\1 \3', inputString).lower()
    inputString = re.sub(r'(\w)(\'|")(\s|$)', r'\1 \3', inputString)
    inputString = re.sub(r'(\s|^)(\'|")(\w)', r'\1 \3', inputString)

    startpos = 0  # the start position in the inputString during the loop

    # list of lists in format:
    # [startpos, endpos, matchedstring, flags, type]
    matches = []

    while startpos < len(inputString):

        # empty match
        leftmost_match = [0, 0, None, 0, None]

        # Modifier like next\prev..
        m = ptc.CRE_MODIFIER.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start() + startpos:
                leftmost_match[0] = m.start() + startpos
                leftmost_match[1] = m.end() + startpos
                leftmost_match[2] = m.group()
                leftmost_match[3] = 0
                leftmost_match[4] = 'modifier'

        # Quantity + Units
        m = ptc.CRE_UNITS.search(inputString[startpos:])
        if m is not None:
            debug and logging.debug('CRE_UNITS matched')
            if _UnitsTrapped(ptc, inputString[startpos:], m, 'units'):
                debug and logging.debug('day suffix trapped by unit match')
            else:

                if leftmost_match[1] == 0 or \
                        leftmost_match[0] > m.start('qty') + startpos:
                    leftmost_match[0] = m.start('qty') + startpos
                    leftmost_match[1] = m.end('qty') + startpos
                    leftmost_match[2] = m.group('qty')
                    leftmost_match[3] = 3
                    leftmost_match[4] = 'units'

                    if m.start('qty') > 0 and \
                            inputString[m.start('qty') - 1] == '-':
                        leftmost_match[0] = leftmost_match[0] - 1
                        leftmost_match[2] = '-' + leftmost_match[2]

        # Quantity + Units
        m = ptc.CRE_QUNITS.search(inputString[startpos:])
        if m is not None:
            debug and logging.debug('CRE_QUNITS matched')
            if _UnitsTrapped(ptc, inputString[startpos:], m, 'qunits'):
                debug and logging.debug('day suffix trapped by qunit match')
            else:
                if leftmost_match[1] == 0 or \
                        leftmost_match[0] > m.start('qty') + startpos:
                    leftmost_match[0] = m.start('qty') + startpos
                    leftmost_match[1] = m.end('qty') + startpos
                    leftmost_match[2] = m.group('qty')
                    leftmost_match[3] = 3
                    leftmost_match[4] = 'qunits'

                    if m.start('qty') > 0 and \
                            inputString[m.start('qty') - 1] == '-':
                        leftmost_match[0] = leftmost_match[0] - 1
                        leftmost_match[2] = '-' + leftmost_match[2]

        m = ptc.CRE_DATE3.search(inputString[startpos:])

        # String date format
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start('date') + startpos:
                leftmost_match[0] = m.start('date') + startpos
                leftmost_match[1] = m.end('date') + startpos
                leftmost_match[2] = m.group('date')
                leftmost_match[3] = 1
                leftmost_match[4] = 'dateStr'

        # Standard date format
        m = ptc.CRE_DATE.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start('date') + startpos:
                leftmost_match[0] = m.start('date') + startpos
                leftmost_match[1] = m.end('date') + startpos
                leftmost_match[2] = m.group('date')
                leftmost_match[3] = 1
                leftmost_match[4] = 'dateStd'

        # Natural language day strings
        m = ptc.CRE_DAY.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start() + startpos:
                leftmost_match[0] = m.start() + startpos
                leftmost_match[1] = m.end() + startpos
                leftmost_match[2] = m.group()
                leftmost_match[3] = 1
                leftmost_match[4] = 'dayStr'

        # Weekday
        m = ptc.CRE_WEEKDAY.search(inputString[startpos:])
        if m is not None:
            if inputString[startpos:] not in ptc.dayOffsets:
                if leftmost_match[1] == 0 or \
                        leftmost_match[0] > m.start() + startpos:
                    leftmost_match[0] = m.start() + startpos
                    leftmost_match[1] = m.end() + startpos
                    leftmost_match[2] = m.group()
                    leftmost_match[3] = 1
                    leftmost_match[4] = 'weekdy'

        # Natural language time strings
        m = ptc.CRE_TIME.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start() + startpos:
                leftmost_match[0] = m.start() + startpos
                leftmost_match[1] = m.end() + startpos
                leftmost_match[2] = m.group()
                leftmost_match[3] = 2
                leftmost_match[4] = 'timeStr'

        # HH:MM(:SS) am/pm time strings
        m = ptc.CRE_TIMEHMS2.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start('hours') + startpos:
                leftmost_match[0] = m.start('hours') + startpos
                leftmost_match[1] = m.end('meridian') + startpos
                leftmost_match[2] = inputString[leftmost_match[0]:
                                                leftmost_match[1]]
                leftmost_match[3] = 2
                leftmost_match[4] = 'meridian'

        # HH:MM(:SS) time strings
        m = ptc.CRE_TIMEHMS.search(inputString[startpos:])
        if m is not None:
            if leftmost_match[1] == 0 or \
                    leftmost_match[0] > m.start('hours') + startpos:
                leftmost_match[0] = m.start('hours') + startpos
                if m.group('seconds') is not None:
                    leftmost_match[1] = m.end('seconds') + startpos
                else:
                    leftmost_match[1] = m.end('minutes') + startpos
                leftmost_match[2] = inputString[leftmost_match[0]:
                                                leftmost_match[1]]
                leftmost_match[3] = 2
                leftmost_match[4] = 'timeStd'

        # Units only; must be preceded by a modifier
        if len(matches) > 0 and matches[-1][3] == 0:
            m = ptc.CRE_UNITS_ONLY.search(inputString[startpos:])
            # Ensure that any match is immediately preceded by the
            # modifier. "Next is the word 'month'" should not parse as a
            # date while "next month" should
            if m is not None and \
                    inputString[startpos:startpos + m.start()].strip() == '':
                debug and logging.debug(f'CRE_UNITS_ONLY matched [{m.group()}]')
                if leftmost_match[1] == 0 or \
                        leftmost_match[0] > m.start() + startpos:
                    leftmost_match[0] = m.start() + startpos
                    leftmost_match[1] = m.end() + startpos
                    leftmost_match[2] = m.group()
                    leftmost_match[3] = 3
                    leftmost_match[4] = 'unitsOnly'

        # set the start position to the end pos of the leftmost match
        startpos = leftmost_match[1]

        # nothing was detected
        # so break out of the loop
        if startpos == 0:
            startpos = len(inputString)
        else:
            if leftmost_match[3] > 0:
                m = ptc.CRE_NLP_PREFIX.search(
                    inputString[:leftmost_match[0]] + ' ' + str(leftmost_match[3]))
                if m is not None:
                    leftmost_match[0] = m.start('nlp_prefix')
                    leftmost_match[2] = inputString[leftmost_match[0]:
                                                    leftmost_match[1]]
            matches.append(leftmost_match)

    # find matches in proximity with one another and
    # return all the parsed values
    proximity_matches = []
    if len(matches) > 1:
        combined = ''
        from_match_index = 0
        date = matches[0][3] == 1
        time_ = matches[0][3] == 2
        units = matches[0][3] == 3
        for i in range(1, len(matches)):

            # test proximity (are there characters between matches?)
            endofprevious = matches[i - 1][1]
            begofcurrent = matches[i][0]
            if orig_inputstring[endofprevious:
                                begofcurrent].lower().strip() != '':
                # this one isn't in proximity, but maybe
                # we have enough to make a datetime
                # TODO: make sure the combination of
                # formats (modifier, dateStd, etc) makes logical sense
                # before parsing together
                if date or time_ or units:
                    combined = orig_inputstring[matches[from_match_index]
                                                [0]:matches[i - 1][1]]
                    parsed_datetime, flags = calendar.parse(combined,
                                                        sourceTime,
                                                        version)
                    proximity_matches.append((
                        datetime.datetime(*parsed_datetime[:6]),
                        flags,
                        matches[from_match_index][0],
                        matches[i - 1][1],
                        combined))
                # not in proximity, reset starting from current
                from_match_index = i
                date = matches[i][3] == 1
                time_ = matches[i][3] == 2
                units = matches[i][3] == 3
                continue
            else:
                if matches[i][3] == 1:
                    date = True
                if matches[i][3] == 2:
                    time_ = True
                if matches[i][3] == 3:
                    units = True

        # check last
        # we have enough to make a datetime
        if date or time_ or units:
            combined = orig_inputstring[matches[from_match_index][0]:
                                        matches[len(matches) - 1][1]]
            parsed_datetime, flags = calendar.parse(combined, sourceTime,
                                                version)
            proximity_matches.append((
                datetime.datetime(*parsed_datetime[:6]),
                flags,
                matches[from_match_index][0],
                matches[len(matches) - 1][1],
                combined))

    elif len(matches) == 0:
        return None
    else:
        if matches[0][3] == 0:  # not enough info to parse
            return None
        else:
            combined = orig_inputstring[matches[0][0]:matches[0][1]]
            parsed_datetime, flags = calendar.parse(matches[0][2], sourceTime,
                                                version)
            proximity_matches.append((
                datetime.datetime(*parsed_datetime[:6]),
                flags,
                matches[0][0],
                matches[0][1],
                combined))

    return tuple(proximity_matches)
