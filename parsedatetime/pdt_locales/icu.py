# -*- encoding: utf-8 -*-

"""
pdt_locales

All of the included locale classes shipped with pdt.
"""
import datetime

from six.moves import range

try:
    import PyICU as pyicu
except:
    pyicu = None

__all__ = [
    'get_icu',
]


def lcase(x):
    return x.lower()


def get_icu(locale):
    result = {}
    icu = None
    if pyicu is not None:
        if locale is None:
            locale = 'en_US'
        icu = pyicu.Locale(locale)

    if icu is not None:

        # grab spelled out format of all numbers from 0 to 100
        rbnf = pyicu.RuleBasedNumberFormat(pyicu.URBNFRuleSetTag.SPELLOUT, icu)
        result['numbers'] = dict([(rbnf.format(i), i) for i in range(0, 100)])

        symbols = result['symbols'] = pyicu.DateFormatSymbols(icu)

        # grab ICU list of weekdays, skipping first entry which
        # is always blank
        wd = list(map(lcase, symbols.getWeekdays()[1:]))
        swd = list(map(lcase, symbols.getShortWeekdays()[1:]))

        # store them in our list with Monday first (ICU puts Sunday first)
        result['Weekdays'] = wd[1:] + wd[0:1]
        result['shortWeekdays'] = swd[1:] + swd[0:1]
        result['Months'] = list(map(lcase, symbols.getMonths()))
        result['shortMonths'] = list(map(lcase, symbols.getShortMonths()))
        keys = ['full', 'long', 'medium', 'short']

        icu_df = result['icu_df'] = {'full': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kFull, icu),
                                     'long': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kLong, icu),
                                     'medium': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kMedium, icu),
                                     'short': pyicu.DateFormat.createDateInstance(pyicu.DateFormat.kShort, icu),
                                     }
        icu_tf = result['icu_tf'] = {'full': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kFull, icu),
                                     'long': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kLong, icu),
                                     'medium': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kMedium, icu),
                                     'short': pyicu.DateFormat.createTimeInstance(pyicu.DateFormat.kShort, icu),
                                     }

        result['dateFormats'] = {x: icu_df[x].toPattern() for x in keys}
        result['timeFormats'] = {x: icu_tf[x].toPattern() for x in keys}

        am = ''
        pm = ''
        ts = ''

        # ICU doesn't seem to provide directly the date or time separator
        # so we have to figure it out
        o = result['icu_tf']['short']
        s = result['timeFormats']['short']

        result['usesMeridian'] = 'a' in s
        result['uses24'] = 'H' in s

        # '11:45 AM' or '11:45'
        s = o.format(datetime.datetime(2003, 10, 30, 11, 45))

        # ': AM' or ':'
        s = s.replace('11', '').replace('45', '')

        if len(s) > 0:
            ts = s[0]

        if result['usesMeridian']:
            # '23:45 AM' or '23:45'
            am = s[1:].strip()
            s = o.format(datetime.datetime(2003, 10, 30, 23, 45))

            if result['uses24']:
                s = s.replace('23', '')
            else:
                s = s.replace('11', '')

                # 'PM' or ''
            pm = s.replace('45', '').replace(ts, '').strip()

        result['timeSep'] = [ts]
        result['meridian'] = [am, pm]

        o = result['icu_df']['short']
        s = o.format(datetime.datetime(2003, 10, 30, 11, 45))
        s = s.replace('10', '').replace('30', '').replace('03', '').replace('2003', '')

        if len(s) > 0:
            ds = s[0]
        else:
            ds = '/'

        result['dateSep'] = [ds]
        s = result['dateFormats']['short']
        l = s.lower().split(ds)
        dp_order = []

        for s in l:
            if len(s) > 0:
                dp_order.append(s[:1])

        result['dp_order'] = dp_order
    return result
