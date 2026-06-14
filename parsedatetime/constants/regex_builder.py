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

"""parsedatetime.constants.regex_builder — regex pattern construction

Extracted from the Constants class __init__, this module builds all the
RE_* regex string templates used by parsedatetime.
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re


def _getLocaleDataAdjusted(localeData):
    """
    If localeData is defined as ["mon|mnd", 'tu|tues'...] then this
    function splits those definitions on |
    """
    adjusted = []
    for d in localeData:
        if '|' in d:
            adjusted += d.split("|")
        else:
            adjusted.append(d)
    return adjusted


def re_join(g):
    return '|'.join(re.escape(i) for i in g)


def _buildOffsets(offsetDict, localeData, indexStart):
    o = indexStart
    for key in localeData:
        if '|' in key:
            for k in key.split('|'):
                offsetDict[k] = o
        else:
            offsetDict[key] = o
        o += 1


def build_regex_patterns(ptc):
    """
    Build all RE_* regex pattern strings and set them as attributes
    on the given Constants instance (ptc).

    This extracts the regex-building logic from Constants.__init__()
    into a standalone function.

    @type  ptc: Constants
    @param ptc: The Constants instance to populate with regex patterns
    """
    mths = _getLocaleDataAdjusted(ptc.locale.Months)
    smths = _getLocaleDataAdjusted(ptc.locale.shortMonths)
    swds = _getLocaleDataAdjusted(ptc.locale.shortWeekdays)
    wds = _getLocaleDataAdjusted(ptc.locale.Weekdays)

    # escape any regex special characters that may be found
    ptc.locale.re_values['months'] = re_join(mths)
    ptc.locale.re_values['shortmonths'] = re_join(smths)
    ptc.locale.re_values['days'] = re_join(wds)
    ptc.locale.re_values['shortdays'] = re_join(swds)
    ptc.locale.re_values['dayoffsets'] = \
        re_join(ptc.locale.dayOffsets)
    ptc.locale.re_values['numbers'] = \
        re_join(ptc.locale.numbers)
    ptc.locale.re_values['decimal_mark'] = \
        re.escape(ptc.locale.decimal_mark)

    units = [unit for units in ptc.locale.units.values()
             for unit in units]  # flatten
    units.sort(key=len, reverse=True)  # longest first
    ptc.locale.re_values['units'] = re_join(units)
    ptc.locale.re_values['modifiers'] = re_join(ptc.locale.Modifiers)
    ptc.locale.re_values['sources'] = re_join(ptc.locale.re_sources)

    # For distinguishing numeric dates from times, look for timeSep
    # and meridian, if specified in the locale
    ptc.locale.re_values['timecomponents'] = \
        re_join(ptc.locale.timeSep + ptc.locale.meridian)

    # build weekday offsets
    _buildOffsets(ptc.locale.WeekdayOffsets,
                  ptc.locale.Weekdays, 0)
    _buildOffsets(ptc.locale.WeekdayOffsets,
                  ptc.locale.shortWeekdays, 0)

    # build month offsets
    _buildOffsets(ptc.locale.MonthOffsets,
                  ptc.locale.Months, 1)
    _buildOffsets(ptc.locale.MonthOffsets,
                  ptc.locale.shortMonths, 1)

    # ─── Build RE_* pattern strings ──────────────────────────────────────

    # not being used in code, but kept in case others are manually
    # utilizing this regex for their own purposes
    ptc.RE_DATE4 = r'''(?P<date>
                            (
                                (
                                    (?P<day>\d\d?)
                                    (?P<suffix>{daysuffix})?
                                    (,)?
                                    (\s)*
                                )
                                (?P<mthname>
                                    \b({months}|{shortmonths})\b
                                )\s*
                                (?P<year>\d\d
                                    (\d\d)?
                                )?
                            )
                        )'''.format(**ptc.locale.re_values)

    # still not completely sure of the behavior of the regex and
    # whether it would be best to consume all possible irrelevant
    # characters before the option groups (but within the {1,3} repetition
    # group or inside of each option group, as it currently does
    # however, right now, all tests are passing that were,
    # including fixing the bug of matching a 4-digit year as ddyy
    # when the day is absent from the string
    ptc.RE_DATE3 = r'''(?P<date>
                            (?:
                                (?:^|\s+)
                                (?P<mthname>
                                    {months}|{shortmonths}
                                )\b
                                |
                                (?:^|\s+)
                                (?P<day>[1-9]|[012]\d|3[01])
                                (?P<suffix>{daysuffix}|)\b
                                (?!\s*(?:{timecomponents}))
                                |
                                ,?\s+
                                (?P<year>\d\d(?:\d\d|))\b
                                (?!\s*(?:{timecomponents}))
                            ){{1,3}}
                            (?(mthname)|$-^)
                        )'''.format(**ptc.locale.re_values)

    # not being used in code, but kept in case others are manually
    # utilizing this regex for their own purposes
    ptc.RE_MONTH = r'''(\s+|^)
                        (?P<month>
                            (
                                (?P<mthname>
                                    \b({months}|{shortmonths})\b
                                )
                                (\s*
                                    (?P<year>(\d{{4}}))
                                )?
                            )
                        )
                        (?=\s+|$|[^\w])'''.format(**ptc.locale.re_values)

    ptc.RE_WEEKDAY = r'''\b
                          (?:
                              {days}|{shortdays}
                          )
                          \b'''.format(**ptc.locale.re_values)

    ptc.RE_NUMBER = (r'(\b(?:{numbers})\b|\d+(?:{decimal_mark}\d+|))'
                     .format(**ptc.locale.re_values))

    ptc.RE_SPECIAL = (r'(?P<special>^[{specials}]+)\s+'
                      .format(**ptc.locale.re_values))

    ptc.RE_UNITS_ONLY = (r'''\b({units})\b'''
                         .format(**ptc.locale.re_values))

    ptc.RE_UNITS = r'''\b(?P<qty>
                            -?
                            (?:\d+(?:{decimal_mark}\d+|)|(?:{numbers})\b)\s*
                            (?P<units>{units})
                        )\b'''.format(**ptc.locale.re_values)

    ptc.RE_QUNITS = r'''\b(?P<qty>
                             -?
                             (?:\d+(?:{decimal_mark}\d+|)|(?:{numbers})\s+)\s*
                             (?P<qunits>{qunits})
                         )\b'''.format(**ptc.locale.re_values)

    ptc.RE_MODIFIER = r'''\b(?:
                               {modifiers}
                           )\b'''.format(**ptc.locale.re_values)

    ptc.RE_TIMEHMS = r'''([\s(\["'-]|^)
                          (?P<hours>\d\d?)
                          (?P<tsep>{timeseparator}|)
                          (?P<minutes>\d\d)
                          (?:(?P=tsep)
                              (?P<seconds>\d\d
                                  (?:[\.,]\d+)?
                              )
                          )?\b'''.format(**ptc.locale.re_values)

    ptc.RE_TIMEHMS2 = r'''([\s(\["'-]|^)
                           (?P<hours>\d\d?)
                           (?:
                               (?P<tsep>{timeseparator}|)
                               (?P<minutes>\d\d?)
                               (?:(?P=tsep)
                                   (?P<seconds>\d\d?
                                       (?:[\.,]\d+)?
                                   )
                               )?
                           )?'''.format(**ptc.locale.re_values)

    # 1, 2, and 3 here refer to the type of match date, time, or units
    ptc.RE_NLP_PREFIX = r'''\b(?P<nlp_prefix>
                              (on)
                              (\s)+1
                              |
                              (at|in)
                              (\s)+2
                              |
                              (in)
                              (\s)+3
                             )'''

    if 'meridian' in ptc.locale.re_values:
        ptc.RE_TIMEHMS2 += (r'\s*(?P<meridian>{meridian})\b'
                            .format(**ptc.locale.re_values))
    else:
        ptc.RE_TIMEHMS2 += r'\b'

    # Always support common . and - separators
    dateSeps = ''.join(re.escape(s)
                       for s in ptc.locale.dateSep + ['-', '.'])

    ptc.RE_DATE = r'''([\s(\["'-]|^)
                       (?P<date>
                            \d\d?[{0}]\d\d?(?:[{0}]\d\d(?:\d\d)?)?
                            |
                            \d{{4}}[{0}]\d\d?[{0}]\d\d?
                        )
                       \b'''.format(dateSeps)

    ptc.RE_DATE2 = r'[{0}]'.format(dateSeps)

    assert 'dayoffsets' in ptc.locale.re_values

    ptc.RE_DAY = r'''\b
                      (?:
                          {dayoffsets}
                      )
                      \b'''.format(**ptc.locale.re_values)

    ptc.RE_DAY2 = r'''(?P<day>\d\d?)
                       (?P<suffix>{daysuffix})?
                   '''.format(**ptc.locale.re_values)

    ptc.RE_TIME = r'''\b
                       (?:
                           {sources}
                       )
                       \b'''.format(**ptc.locale.re_values)

    ptc.RE_REMAINING = r'\s+'

    # Regex for date/time ranges
    ptc.RE_RTIMEHMS = r'''(\s*|^)
                           (\d\d?){timeseparator}
                           (\d\d)
                           ({timeseparator}(\d\d))?
                           (\s*|$)'''.format(**ptc.locale.re_values)

    ptc.RE_RTIMEHMS2 = (r'''(\s*|^)
                             (\d\d?)
                             ({timeseparator}(\d\d?))?
                             ({timeseparator}(\d\d?))?'''
                         .format(**ptc.locale.re_values))

    if 'meridian' in ptc.locale.re_values:
        ptc.RE_RTIMEHMS2 += (r'\s*({meridian})'
                              .format(**ptc.locale.re_values))

    ptc.RE_RDATE = r'(\d+([%s]\d+)+)' % dateSeps
    ptc.RE_RDATE3 = r'''(
                            (
                                (
                                    \b({months})\b
                                )\s*
                                (
                                    (\d\d?)
                                    (\s?|{daysuffix}|$)+
                                )?
                                (,\s*\d{{4}})?
                            )
                        )'''.format(**ptc.locale.re_values)

    # "06/07/06 - 08/09/06"
    ptc.DATERNG1 = (r'{0}\s*{rangeseparator}\s*{0}'
                    .format(ptc.RE_RDATE, **ptc.locale.re_values))

    # "march 31 - june 1st, 2006"
    ptc.DATERNG2 = (r'{0}\s*{rangeseparator}\s*{0}'
                    .format(ptc.RE_RDATE3, **ptc.locale.re_values))

    # "march 1rd -13th"
    ptc.DATERNG3 = (r'{0}\s*{rangeseparator}\s*(\d\d?)\s*(rd|st|nd|th)?'
                    .format(ptc.RE_RDATE3, **ptc.locale.re_values))

    # "4:00:55 pm - 5:90:44 am", '4p-5p'
    ptc.TIMERNG1 = (r'{0}\s*{rangeseparator}\s*{0}'
                    .format(ptc.RE_RTIMEHMS2, **ptc.locale.re_values))

    ptc.TIMERNG2 = (r'{0}\s*{rangeseparator}\s*{0}'
                    .format(ptc.RE_RTIMEHMS, **ptc.locale.re_values))

    # "4-5pm "
    ptc.TIMERNG3 = (r'\d\d?\s*{rangeseparator}\s*{0}'
                    .format(ptc.RE_RTIMEHMS2, **ptc.locale.re_values))

    # "4:30-5pm "
    ptc.TIMERNG4 = (r'{0}\s*{rangeseparator}\s*{1}'
                    .format(ptc.RE_RTIMEHMS, ptc.RE_RTIMEHMS2,
                            **ptc.locale.re_values))

    ptc.re_option = re.IGNORECASE + re.VERBOSE
    ptc.cre_source = {'CRE_SPECIAL': ptc.RE_SPECIAL,
                       'CRE_NUMBER': ptc.RE_NUMBER,
                       'CRE_UNITS': ptc.RE_UNITS,
                       'CRE_UNITS_ONLY': ptc.RE_UNITS_ONLY,
                       'CRE_QUNITS': ptc.RE_QUNITS,
                       'CRE_MODIFIER': ptc.RE_MODIFIER,
                       'CRE_TIMEHMS': ptc.RE_TIMEHMS,
                       'CRE_TIMEHMS2': ptc.RE_TIMEHMS2,
                       'CRE_DATE': ptc.RE_DATE,
                       'CRE_DATE2': ptc.RE_DATE2,
                       'CRE_DATE3': ptc.RE_DATE3,
                       'CRE_DATE4': ptc.RE_DATE4,
                       'CRE_MONTH': ptc.RE_MONTH,
                       'CRE_WEEKDAY': ptc.RE_WEEKDAY,
                       'CRE_DAY': ptc.RE_DAY,
                       'CRE_DAY2': ptc.RE_DAY2,
                       'CRE_TIME': ptc.RE_TIME,
                       'CRE_REMAINING': ptc.RE_REMAINING,
                       'CRE_RTIMEHMS': ptc.RE_RTIMEHMS,
                       'CRE_RTIMEHMS2': ptc.RE_RTIMEHMS2,
                       'CRE_RDATE': ptc.RE_RDATE,
                       'CRE_RDATE3': ptc.RE_RDATE3,
                       'CRE_TIMERNG1': ptc.TIMERNG1,
                       'CRE_TIMERNG2': ptc.TIMERNG2,
                       'CRE_TIMERNG3': ptc.TIMERNG3,
                       'CRE_TIMERNG4': ptc.TIMERNG4,
                       'CRE_DATERNG1': ptc.DATERNG1,
                       'CRE_DATERNG2': ptc.DATERNG2,
                       'CRE_DATERNG3': ptc.DATERNG3,
                       'CRE_NLP_PREFIX': ptc.RE_NLP_PREFIX}
    ptc.cre_keys = set(ptc.cre_source.keys())
