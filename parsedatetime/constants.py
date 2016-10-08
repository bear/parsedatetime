# -*- coding: utf-8 -*-
"""
parsedatetime/constants.py

Class handling the loading and initialization of locale aware regexes
as well as the parsing configuration used in Calendar
"""

import re
import logging
import calendar

from .locales import (locales as _locales, get_icu, load_locale)
from .warns import pdt20DeprecationWarning


debug = False
log = logging.getLogger(__name__)

pdtLocales = dict([(x, load_locale(x)) for x in _locales])


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
        # from the given SourceTime, otherwise it will be 9am

        self.StartTimeFromSourceTime = False

        # YearParseStyle controls how we parse "Jun 12", i.e. dates that do
        # not have a year present.  The default is to compare the date given
        # to the current date, and if prior, then assume the next year.
        # Setting this to 0 will prevent that.

        self.YearParseStyle = 1

        # DOWParseStyle controls how we parse "Tuesday"
        # If the current day was Thursday and the text to parse is "Tuesday"
        # then the following table shows how each style would be returned
        # -1, 0, +1
        #
        # Current day marked as ***
        #
        #          Sun Mon Tue Wed Thu Fri Sat
        # week -1
        # current         -1,0     ***
        # week +1          +1
        #
        # If the current day was Monday and the text to parse is "Tuesday"
        # then the following table shows how each style would be returned
        # -1, 0, +1
        #
        #          Sun Mon Tue Wed Thu Fri Sat
        # week -1           -1
        # current      *** 0,+1
        # week +1

        self.DOWParseStyle = 1

        # CurrentDOWParseStyle controls how we parse "Friday"
        # If the current day was Friday and the text to parse is "Friday"
        # then the following table shows how each style would be returned
        # True/False. This also depends on DOWParseStyle.
        #
        # Current day marked as ***
        #
        # DOWParseStyle = 0
        #          Sun Mon Tue Wed Thu Fri Sat
        # week -1
        # current                      T,F
        # week +1
        #
        # DOWParseStyle = -1
        #          Sun Mon Tue Wed Thu Fri Sat
        # week -1                       F
        # current                       T
        # week +1
        #
        # DOWParseStyle = +1
        #
        #          Sun Mon Tue Wed Thu Fri Sat
        # week -1
        # current                       T
        # week +1                       F

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

            mths = _getLocaleDataAdjusted(self.locale.Months)
            smths = _getLocaleDataAdjusted(self.locale.shortMonths)
            swds = _getLocaleDataAdjusted(self.locale.shortWeekdays)
            wds = _getLocaleDataAdjusted(self.locale.Weekdays)

            # escape any regex special characters that may be found
            self.locale.re_values['months'] = re_join(mths)
            self.locale.re_values['shortmonths'] = re_join(smths)
            self.locale.re_values['days'] = re_join(wds)
            self.locale.re_values['shortdays'] = re_join(swds)
            self.locale.re_values['dayoffsets'] = \
                re_join(self.locale.dayOffsets)
            self.locale.re_values['numbers'] = \
                re_join(self.locale.numbers)
            self.locale.re_values['decimal_mark'] = \
                re.escape(self.locale.decimal_mark)

            units = [unit for units in self.locale.units.values()
                     for unit in units]  # flatten
            units.sort(key=len, reverse=True)  # longest first
            self.locale.re_values['units'] = re_join(units)
            self.locale.re_values['modifiers'] = re_join(self.locale.Modifiers)
            self.locale.re_values['sources'] = re_join(self.locale.re_sources)

            # For distinguishing numeric dates from times, look for timeSep
            # and meridian, if specified in the locale
            self.locale.re_values['timecomponents'] = \
                re_join(self.locale.timeSep + self.locale.meridian)

            # build weekday offsets - yes, it assumes the Weekday and
            # shortWeekday lists are in the same order and Mon..Sun
            # (Python style)
            def _buildOffsets(offsetDict, localeData, indexStart):
                o = indexStart
                for key in localeData:
                    if '|' in key:
                        for k in key.split('|'):
                            offsetDict[k] = o
                    else:
                        offsetDict[key] = o
                    o += 1

            _buildOffsets(self.locale.WeekdayOffsets,
                          self.locale.Weekdays, 0)
            _buildOffsets(self.locale.WeekdayOffsets,
                          self.locale.shortWeekdays, 0)

            # build month offsets - yes, it assumes the Months and shortMonths
            # lists are in the same order and Jan..Dec
            _buildOffsets(self.locale.MonthOffsets,
                          self.locale.Months, 1)
            _buildOffsets(self.locale.MonthOffsets,
                          self.locale.shortMonths, 1)

        # build am and pm lists to contain
        # original case, lowercase, first-char and dotted
        # versions of the meridian text
        self.am = ['', '']
        self.pm = ['', '']
        for idx, xm in enumerate(self.locale.meridian[:2]):
            # 0: am
            # 1: pm
            target = ['am', 'pm'][idx]
            setattr(self, target, [xm])
            target = getattr(self, target)
            if xm:
                lxm = xm.lower()
                target.extend((xm[0], '{0}.{1}.'.format(*xm),
                               lxm, lxm[0], '{0}.{1}.'.format(*lxm)))

        # TODO: add code to parse the date formats and build the regexes up
        # from sub-parts, find all hard-coded uses of date/time separators

        # not being used in code, but kept in case others are manually
        # utilizing this regex for their own purposes
        self.RE_DATE4 = r'''(?P<date>
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
                            )'''.format(**self.locale.re_values)

        # still not completely sure of the behavior of the regex and
        # whether it would be best to consume all possible irrelevant
        # characters before the option groups (but within the {1,3} repetition
        # group or inside of each option group, as it currently does
        # however, right now, all tests are passing that were,
        # including fixing the bug of matching a 4-digit year as ddyy
        # when the day is absent from the string
        self.RE_DATE3 = r'''(?P<date>
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
                            )'''.format(**self.locale.re_values)

        # not being used in code, but kept in case others are manually
        # utilizing this regex for their own purposes
        self.RE_MONTH = r'''(\s+|^)
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
                            (?=\s+|$|[^\w])'''.format(**self.locale.re_values)

        self.RE_WEEKDAY = r'''\b
                              (?:
                                  {days}|{shortdays}
                              )
                              \b'''.format(**self.locale.re_values)

        self.RE_NUMBER = (r'(\b(?:{numbers})\b|\d+(?:{decimal_mark}\d+|))'
                          .format(**self.locale.re_values))

        self.RE_SPECIAL = (r'(?P<special>^[{specials}]+)\s+'
                           .format(**self.locale.re_values))

        self.RE_UNITS_ONLY = (r'''\b({units})\b'''
                              .format(**self.locale.re_values))

        self.RE_UNITS = r'''\b(?P<qty>
                                -?
                                (?:\d+(?:{decimal_mark}\d+|)|(?:{numbers})\b)\s*
                                (?P<units>{units})
                            )\b'''.format(**self.locale.re_values)

        self.RE_QUNITS = r'''\b(?P<qty>
                                 -?
                                 (?:\d+(?:{decimal_mark}\d+|)|(?:{numbers})\s+)\s*
                                 (?P<qunits>{qunits})
                             )\b'''.format(**self.locale.re_values)

        self.RE_MODIFIER = r'''\b(?:
                                   {modifiers}
                               )\b'''.format(**self.locale.re_values)

        self.RE_TIMEHMS = r'''([\s(\["'-]|^)
                              (?P<hours>\d\d?)
                              (?P<tsep>{timeseparator}|)
                              (?P<minutes>\d\d)
                              (?:(?P=tsep)
                                  (?P<seconds>\d\d
                                      (?:[\.,]\d+)?
                                  )
                              )?\b'''.format(**self.locale.re_values)

        self.RE_TIMEHMS2 = r'''([\s(\["'-]|^)
                               (?P<hours>\d\d?)
                               (?:
                                   (?P<tsep>{timeseparator}|)
                                   (?P<minutes>\d\d?)
                                   (?:(?P=tsep)
                                       (?P<seconds>\d\d?
                                           (?:[\.,]\d+)?
                                       )
                                   )?
                               )?'''.format(**self.locale.re_values)

        # 1, 2, and 3 here refer to the type of match date, time, or units
        self.RE_NLP_PREFIX = r'''\b(?P<nlp_prefix>
                                  (on)
                                  (\s)+1
                                  |
                                  (at|in)
                                  (\s)+2
                                  |
                                  (in)
                                  (\s)+3
                                 )'''

        if 'meridian' in self.locale.re_values:
            self.RE_TIMEHMS2 += (r'\s*(?P<meridian>{meridian})\b'
                                 .format(**self.locale.re_values))
        else:
            self.RE_TIMEHMS2 += r'\b'

        # Always support common . and - separators
        dateSeps = ''.join(re.escape(s)
                           for s in self.locale.dateSep + ['-', '.'])

        self.RE_DATE = r'''([\s(\["'-]|^)
                           (?P<date>
                                \d\d?[{0}]\d\d?(?:[{0}]\d\d(?:\d\d)?)?
                                |
                                \d{{4}}[{0}]\d\d?[{0}]\d\d?
                            )
                           \b'''.format(dateSeps)

        self.RE_DATE2 = r'[{0}]'.format(dateSeps)

        assert 'dayoffsets' in self.locale.re_values

        self.RE_DAY = r'''\b
                          (?:
                              {dayoffsets}
                          )
                          \b'''.format(**self.locale.re_values)

        self.RE_DAY2 = r'''(?P<day>\d\d?)
                           (?P<suffix>{daysuffix})?
                       '''.format(**self.locale.re_values)

        self.RE_TIME = r'''\b
                           (?:
                               {sources}
                           )
                           \b'''.format(**self.locale.re_values)

        self.RE_REMAINING = r'\s+'

        # Regex for date/time ranges
        self.RE_RTIMEHMS = r'''(\s*|^)
                               (\d\d?){timeseparator}
                               (\d\d)
                               ({timeseparator}(\d\d))?
                               (\s*|$)'''.format(**self.locale.re_values)

        self.RE_RTIMEHMS2 = (r'''(\s*|^)
                                 (\d\d?)
                                 ({timeseparator}(\d\d?))?
                                 ({timeseparator}(\d\d?))?'''
                             .format(**self.locale.re_values))

        if 'meridian' in self.locale.re_values:
            self.RE_RTIMEHMS2 += (r'\s*({meridian})'
                                  .format(**self.locale.re_values))

        self.RE_RDATE = r'(\d+([%s]\d+)+)' % dateSeps
        self.RE_RDATE3 = r'''(
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
                            )'''.format(**self.locale.re_values)

        # "06/07/06 - 08/09/06"
        self.DATERNG1 = (r'{0}\s*{rangeseparator}\s*{0}'
                         .format(self.RE_RDATE, **self.locale.re_values))

        # "march 31 - june 1st, 2006"
        self.DATERNG2 = (r'{0}\s*{rangeseparator}\s*{0}'
                         .format(self.RE_RDATE3, **self.locale.re_values))

        # "march 1rd -13th"
        self.DATERNG3 = (r'{0}\s*{rangeseparator}\s*(\d\d?)\s*(rd|st|nd|th)?'
                         .format(self.RE_RDATE3, **self.locale.re_values))

        # "4:00:55 pm - 5:90:44 am", '4p-5p'
        self.TIMERNG1 = (r'{0}\s*{rangeseparator}\s*{0}'
                         .format(self.RE_RTIMEHMS2, **self.locale.re_values))

        self.TIMERNG2 = (r'{0}\s*{rangeseparator}\s*{0}'
                         .format(self.RE_RTIMEHMS, **self.locale.re_values))

        # "4-5pm "
        self.TIMERNG3 = (r'\d\d?\s*{rangeseparator}\s*{0}'
                         .format(self.RE_RTIMEHMS2, **self.locale.re_values))

        # "4:30-5pm "
        self.TIMERNG4 = (r'{0}\s*{rangeseparator}\s*{1}'
                         .format(self.RE_RTIMEHMS, self.RE_RTIMEHMS2,
                                 **self.locale.re_values))

        self.re_option = re.IGNORECASE + re.VERBOSE
        self.cre_source = {'CRE_SPECIAL': self.RE_SPECIAL,
                           'CRE_NUMBER': self.RE_NUMBER,
                           'CRE_UNITS': self.RE_UNITS,
                           'CRE_UNITS_ONLY': self.RE_UNITS_ONLY,
                           'CRE_QUNITS': self.RE_QUNITS,
                           'CRE_MODIFIER': self.RE_MODIFIER,
                           'CRE_TIMEHMS': self.RE_TIMEHMS,
                           'CRE_TIMEHMS2': self.RE_TIMEHMS2,
                           'CRE_DATE': self.RE_DATE,
                           'CRE_DATE2': self.RE_DATE2,
                           'CRE_DATE3': self.RE_DATE3,
                           'CRE_DATE4': self.RE_DATE4,
                           'CRE_MONTH': self.RE_MONTH,
                           'CRE_WEEKDAY': self.RE_WEEKDAY,
                           'CRE_DAY': self.RE_DAY,
                           'CRE_DAY2': self.RE_DAY2,
                           'CRE_TIME': self.RE_TIME,
                           'CRE_REMAINING': self.RE_REMAINING,
                           'CRE_RTIMEHMS': self.RE_RTIMEHMS,
                           'CRE_RTIMEHMS2': self.RE_RTIMEHMS2,
                           'CRE_RDATE': self.RE_RDATE,
                           'CRE_RDATE3': self.RE_RDATE3,
                           'CRE_TIMERNG1': self.TIMERNG1,
                           'CRE_TIMERNG2': self.TIMERNG2,
                           'CRE_TIMERNG3': self.TIMERNG3,
                           'CRE_TIMERNG4': self.TIMERNG4,
                           'CRE_DATERNG1': self.DATERNG1,
                           'CRE_DATERNG2': self.DATERNG2,
                           'CRE_DATERNG3': self.DATERNG3,
                           'CRE_NLP_PREFIX': self.RE_NLP_PREFIX}
        self.cre_keys = set(self.cre_source.keys())

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
        debug and log.debug('daysInMonth(%s, %s)', month, year)
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
