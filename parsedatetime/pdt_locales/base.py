# -*- encoding: utf-8 -*-

from . import *


class pdtLocale_base(object):
    """
    default values for Locales
    """
    locale_keys = set([
        'MonthOffsets', 'Months', 'WeekdayOffsets', 'Weekdays',
        'dateFormats', 'dateSep', 'dayOffsets', 'dp_order',
        'localeID', 'meridian', 'Modifiers', 're_sources', 're_values',
        'shortMonths', 'shortWeekdays', 'timeFormats', 'timeSep', 'units',
        'uses24', 'usesMeridian', 'numbers', 'decimal_mark', 'small',
        'magnitude', 'ignore'])

    def __init__(self):
        self.localeID = None  # don't use a unicode string
        self.dateSep = ['/', '.']
        self.timeSep = [':']
        self.meridian = ['AM', 'PM']
        self.usesMeridian = True
        self.uses24 = True

        self.WeekdayOffsets = {}
        self.MonthOffsets = {}

        # always lowercase any lookup values - helper code expects that
        self.Weekdays = ['monday', 'tuesday', 'wednesday',
                         'thursday', 'friday', 'saturday', 'sunday',
                         ]
        self.shortWeekdays = ['mon', 'tues', 'wed',
                              'thu', 'fri', 'sat', 'sun',
                              ]
        self.Months = ['january', 'february', 'march',
                       'april', 'may', 'june',
                       'july', 'august', 'september',
                       'october', 'november', 'december',
                       ]
        self.shortMonths = ['jan', 'feb', 'mar',
                            'apr', 'may', 'jun',
                            'jul', 'aug', 'sep',
                            'oct', 'nov', 'dec',
                            ]
        # use the same formats as ICU by default
        self.dateFormats = {'full': 'EEEE, MMMM d, yyyy',
                            'long': 'MMMM d, yyyy',
                            'medium': 'MMM d, yyyy',
                            'short': 'M/d/yy',
                            }
        self.timeFormats = {'full': 'h:mm:ss a z',
                            'long': 'h:mm:ss a z',
                            'medium': 'h:mm:ss a',
                            'short': 'h:mm a',
                            }

        self.dp_order = ['m', 'd', 'y']

        # Used to parse expressions like "in 5 hours"
        self.numbers = {'zero': 0, 'one': 1, 'a': 1, 'an': 1, 'two': 2, 'three': 3,
                        'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                        'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
                        'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
                        'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
                        'twenty': 20}
        self.decimal_mark = '.'


        # this will be added to re_values later
        self.units = {'seconds': ['second', 'seconds', 'sec', 's'],
                      'minutes': ['minute', 'minutes', 'min', 'm'],
                      'hours': ['hour', 'hours', 'hr', 'h'],
                      'days': ['day', 'days', 'dy', 'd'],
                      'weeks': ['week', 'weeks', 'wk', 'w'],
                      'months': ['month', 'months', 'mth'],
                      'years': ['year', 'years', 'yr', 'y'],
                      }

        # text constants to be used by later regular expressions
        self.re_values = {'specials': 'in|on|of|at',
                          'timeseparator': ':',
                          'rangeseparator': '-',
                          'daysuffix': 'rd|st|nd|th',
                          'meridian': 'am|pm|a.m.|p.m.|a|p',
                          'qunits': 'h|m|s|d|w|y',
                          'now': ['now'],
                          }

        # Used to adjust the returned date before/after the source
        self.Modifiers = {'from': 1,
                          'before': -1,
                          'after': 1,
                          'ago': -1,
                          'prior': -1,
                          'prev': -1,
                          'last': -1,
                          'next': 1,
                          'previous': -1,
                          'end of': 0,
                          'this': 0,
                          'eod': 1,
                          'eom': 1,
                          'eoy': 1,
                          }

        self.dayOffsets = {'tomorrow': 1,
                           'today': 0,
                           'yesterday': -1,
                           }

        # special day and/or times, i.e. lunch, noon, evening
        # each element in the dictionary is a dictionary that is used
        # to fill in any value to be replace - the current date/time will
        # already have been populated by the method buildSources
        self.re_sources = {'noon': {'hr': 12, 'mn': 0, 'sec': 0},
                           'afternoon': {'hr': 13, 'mn': 0, 'sec': 0},
                           'lunch': {'hr': 12, 'mn': 0, 'sec': 0},
                           'morning': {'hr': 6, 'mn': 0, 'sec': 0},
                           'breakfast': {'hr': 8, 'mn': 0, 'sec': 0},
                           'dinner': {'hr': 19, 'mn': 0, 'sec': 0},
                           'evening': {'hr': 18, 'mn': 0, 'sec': 0},
                           'midnight': {'hr': 0, 'mn': 0, 'sec': 0},
                           'night': {'hr': 21, 'mn': 0, 'sec': 0},
                           'tonight': {'hr': 21, 'mn': 0, 'sec': 0},
                           'eod': {'hr': 17, 'mn': 0, 'sec': 0},
                           }

        self.small = {'zero': 0,
                      'one': 1,
                      'a': 1,
                      'an': 1,
                      'two': 2,
                      'three': 3,
                      'four': 4,
                      'five': 5,
                      'six': 6,
                      'seven': 7,
                      'eight': 8,
                      'nine': 9,
                      'ten': 10,
                      'eleven': 11,
                      'twelve': 12,
                      'thirteen': 13,
                      'fourteen': 14,
                      'fifteen': 15,
                      'sixteen': 16,
                      'seventeen': 17,
                      'eighteen': 18,
                      'nineteen': 19,
                      'twenty': 20,
                      'thirty': 30,
                      'forty': 40,
                      'fifty': 50,
                      'sixty': 60,
                      'seventy': 70,
                      'eighty': 80,
                      'ninety': 90
                      }

        self.magnitude = {'thousand': 1000,
                          'million': 1000000,
                          'billion': 1000000000,
                          'trillion': 1000000000000,
                          'quadrillion': 1000000000000000,
                          'quintillion': 1000000000000000000,
                          'sextillion': 1000000000000000000000,
                          'septillion': 1000000000000000000000000,
                          'octillion': 1000000000000000000000000000,
                          'nonillion': 1000000000000000000000000000000,
                          'decillion': 1000000000000000000000000000000000,
                          }

        self.ignore = ('and', ',')


class pdtLocale_icu(pdtLocale_base):
    """
    Create a locale from pyICU
    """

    def __init__(self, localeID):
        super(pdtLocale_icu, self).__init__()

        self.icu = None

        if pyicu is not None:
            if localeID is None:
                localeID = 'en_US'
            self.icu = pyicu.Locale(localeID)

        if self.icu is not None:
            # grab spelled out format of all numbers from 0 to 100
            rbnf = pyicu.RuleBasedNumberFormat(pyicu.URBNFRuleSetTag.SPELLOUT, self.icu)
            try:
                self.numbers = dict([(rbnf.format(i), i) for i in xrange(0, 100)])
            except NameError:
                self.numbers = dict([(rbnf.format(i), i) for i in range(0, 100)])

            self.symbols = pyicu.DateFormatSymbols(self.icu)

            # grab ICU list of weekdays, skipping first entry which
            # is always blank
            wd = list(map(lcase, self.symbols.getWeekdays()[1:]))
            swd = list(map(lcase, self.symbols.getShortWeekdays()[1:]))

            # store them in our list with Monday first (ICU puts Sunday first)
            self.Weekdays = wd[1:] + wd[0:1]
            self.shortWeekdays = swd[1:] + swd[0:1]
            self.Months = list(map(lcase, self.symbols.getMonths()))
            self.shortMonths = list(map(lcase, self.symbols.getShortMonths()))

            self.icu_df = {'full': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kFull, self.icu),
                           'long': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kLong, self.icu),
                           'medium': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kMedium, self.icu),
                           'short': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kShort, self.icu),
                           }
            self.icu_tf = {'full': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kFull, self.icu),
                           'long': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kLong, self.icu),
                           'medium': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kMedium, self.icu),
                           'short': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kShort, self.icu),
                           }
            self.dateFormats = {'full': self.icu_df['full'].toPattern(),
                                'long': self.icu_df['long'].toPattern(),
                                'medium': self.icu_df['medium'].toPattern(),
                                'short': self.icu_df['short'].toPattern(),
                                }
            self.timeFormats = {'full': self.icu_tf['full'].toPattern(),
                                'long': self.icu_tf['long'].toPattern(),
                                'medium': self.icu_tf['medium'].toPattern(),
                                'short': self.icu_tf['short'].toPattern(),
                                }

            am = ''
            pm = ''
            ts = ''

            # ICU doesn't seem to provide directly the date or time separator
            # so we have to figure it out
            o = self.icu_tf['short']
            s = self.timeFormats['short']

            self.usesMeridian = 'a' in s
            self.uses24 = 'H' in s

            # '11:45 AM' or '11:45'
            s = o.format(datetime.datetime(2003, 10, 30, 11, 45))

            # ': AM' or ':'
            s = s.replace('11', '').replace('45', '')

            if len(s) > 0:
                ts = s[0]

            if self.usesMeridian:
                # '23:45 AM' or '23:45'
                am = s[1:].strip()
                s = o.format(datetime.datetime(2003, 10, 30, 23, 45))

                if self.uses24:
                    s = s.replace('23', '')
                else:
                    s = s.replace('11', '')

                    # 'PM' or ''
                pm = s.replace('45', '').replace(ts, '').strip()

            self.timeSep = [ts]
            self.meridian = [am, pm]

            o = self.icu_df['short']
            s = o.format(datetime.datetime(2003, 10, 30, 11, 45))
            s = s.replace('10', '').replace('30', '').replace('03', '').replace('2003', '')

            if len(s) > 0:
                ds = s[0]
            else:
                ds = '/'

            self.dateSep = [ds]
            s = self.dateFormats['short']
            l = s.lower().split(ds)
            dp_order = []

            for s in l:
                if len(s) > 0:
                    dp_order.append(s[:1])

            self.dp_order = dp_order
