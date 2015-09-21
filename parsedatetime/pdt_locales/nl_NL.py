# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base

__all__ = [
    'pdtLocale_nl',
]


class pdtLocale_nl(pdtLocale_base):
    """
    nl_NL Locale constants

    Contributed by Dirkjan Krijnders <dirkjan@krijnders.net>
    """

    def __init__(self):
        super(pdtLocale_nl, self).__init__()

        self.localeID = 'nl_NL'  # don't use a unicode string
        self.dateSep = ['-', '/']
        self.timeSep = [':']
        self.meridian = []
        self.usesMeridian = False
        self.uses24 = True
        self.decimal_mark = ','

        self.Weekdays = ['maandag', 'dinsdag', 'woensdag',
                         'donderdag', 'vrijdag', 'zaterdag', 'zondag',
                         ]
        self.shortWeekdays = ['ma', 'di', 'wo',
                              'do', 'vr', 'za', 'zo',
                              ]
        self.Months = ['januari', 'februari', 'maart',
                       'april', 'mei', 'juni',
                       'juli', 'augustus', 'september',
                       'oktober', 'november', 'december',
                       ]
        self.shortMonths = ['jan', 'feb', 'mar',
                            'apr', 'mei', 'jun',
                            'jul', 'aug', 'sep',
                            'okt', 'nov', 'dec',
                            ]
        self.dateFormats['full'] = 'EEEE, dd MMMM yyyy'
        self.dateFormats['long'] = 'dd MMMM yyyy'
        self.dateFormats['medium'] = 'dd-MM-yyyy'
        self.dateFormats['short'] = 'dd-MM-yy'

        self.timeFormats['full'] = 'HH:mm:ss v'
        self.timeFormats['long'] = 'HH:mm:ss z'
        self.timeFormats['medium'] = 'HH:mm:ss'
        self.timeFormats['short'] = 'HH:mm'

        self.dp_order = ['d', 'm', 'y']

        self.units['seconds'] = ['secunden', 'sec', 's']
        self.units['minutes'] = ['minuten', 'min', 'm']
        self.units['hours'] = ['uren', 'uur', 'h']
        self.units['days'] = ['dagen', 'dag', 'd']
        self.units['weeks'] = ['weken', 'w']
        self.units['months'] = ['maanden', 'maand']  # the short version would be a capital M,
        # as I understand it we can't distinguish
        # between m for minutes and M for months.
        self.units['years'] = ['jaar', 'jaren', 'j']

        self.re_values['specials'] = 'om'
        self.re_values['timeseparator'] = ':'
        self.re_values['rangeseparator'] = '-'
        self.re_values['daysuffix'] = ' |de'
        self.re_values['qunits'] = 'h|m|s|d|w|m|j'
        self.re_values['now'] = ['nu']

        # Used to adjust the returned date before/after the source
        # still looking for insight on how to translate all of them to german.
        self.Modifiers['vanaf'] = 1
        self.Modifiers['voor'] = -1
        self.Modifiers['na'] = 1
        self.Modifiers['vorige'] = -1
        self.Modifiers['eervorige'] = -1
        self.Modifiers['prev'] = -1
        self.Modifiers['laastste'] = -1
        self.Modifiers['volgende'] = 1
        self.Modifiers['deze'] = 0
        self.Modifiers['vorige'] = -1
        self.Modifiers['over'] = 2
        self.Modifiers['eind van'] = 0

        # morgen/abermorgen does not work, see http://code.google.com/p/parsedatetime/issues/detail?id=19
        self.dayOffsets['morgen'] = 1
        self.dayOffsets['vandaag'] = 0
        self.dayOffsets['gisteren'] = -1
        self.dayOffsets['eergisteren'] = -2
        self.dayOffsets['overmorgen'] = 2

        # special day and/or times, i.e. lunch, noon, evening
        # each element in the dictionary is a dictionary that is used
        # to fill in any value to be replace - the current date/time will
        # already have been populated by the method buildSources
        self.re_sources['middag'] = {'hr': 12, 'mn': 0, 'sec': 0}
        self.re_sources['vanmiddag'] = {'hr': 12, 'mn': 0, 'sec': 0}
        self.re_sources['lunch'] = {'hr': 12, 'mn': 0, 'sec': 0}
        self.re_sources['morgen'] = {'hr': 6, 'mn': 0, 'sec': 0}
        self.re_sources['\'s morgens'] = {'hr': 6, 'mn': 0, 'sec': 0}
        self.re_sources['ontbijt'] = {'hr': 8, 'mn': 0, 'sec': 0}
        self.re_sources['avondeten'] = {'hr': 19, 'mn': 0, 'sec': 0}
        self.re_sources['avond'] = {'hr': 18, 'mn': 0, 'sec': 0}
        self.re_sources['avonds'] = {'hr': 18, 'mn': 0, 'sec': 0}
        self.re_sources['middernacht'] = {'hr': 0, 'mn': 0, 'sec': 0}
        self.re_sources['nacht'] = {'hr': 21, 'mn': 0, 'sec': 0}
        self.re_sources['nachts'] = {'hr': 21, 'mn': 0, 'sec': 0}
        self.re_sources['vanavond'] = {'hr': 21, 'mn': 0, 'sec': 0}
        self.re_sources['vannacht'] = {'hr': 21, 'mn': 0, 'sec': 0}
