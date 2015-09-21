# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base

__all__ = [
    'pdtLocale_de',
]

class pdtLocale_de(pdtLocale_base):
    """
    de_DE Locale constants

    Contributed by Debian parsedatetime package maintainer Bernd Zeimetz <bzed@debian.org>
    """
    def __init__(self):
        super( pdtLocale_de, self ).__init__()

        self.localeID      = 'de_DE'   # don't use a unicode string
        self.dateSep       = [ '.' ]
        self.timeSep       = [ ':' ]
        self.meridian      = [ ]
        self.usesMeridian  = False
        self.uses24        = True
        self.decimal_mark = ','

        self.Weekdays      = [ 'montag', 'dienstag', 'mittwoch',
                               'donnerstag', 'freitag', 'samstag', 'sonntag',
                             ]
        self.shortWeekdays = [ 'mo', 'di', 'mi',
                               'do', 'fr', 'sa', 'so',
                             ]
        self.Months        = [ 'januar',  'februar',  'm\xe4rz',
                               'april',   'mai',      'juni',
                               'juli',    'august',   'september',
                               'oktober', 'november', 'dezember',
                             ]
        self.shortMonths   = [ 'jan', 'feb', 'mrz',
                               'apr', 'mai', 'jun',
                               'jul', 'aug', 'sep',
                               'okt', 'nov', 'dez',
                             ]
        self.dateFormats['full']   = 'EEEE, d. MMMM yyyy'
        self.dateFormats['long']   = 'd. MMMM yyyy'
        self.dateFormats['medium'] = 'dd.MM.yyyy'
        self.dateFormats['short']  = 'dd.MM.yy'

        self.timeFormats['full']   = 'HH:mm:ss v'
        self.timeFormats['long']   = 'HH:mm:ss z'
        self.timeFormats['medium'] = 'HH:mm:ss'
        self.timeFormats['short']  = 'HH:mm'

        self.dp_order = [ 'd', 'm', 'y' ]

        self.units['seconds'] = [ 'sekunden', 'sek',  's' ]
        self.units['minutes'] = [ 'minuten',  'min' , 'm' ]
        self.units['hours']   = [ 'stunden',  'std',  'h' ]
        self.units['days']    = [ 'tag',  'tage',     't' ]
        self.units['weeks']   = [ 'wochen',           'w' ]
        self.units['months']  = [ 'monat', 'monate' ]  #the short version would be a capital M,
                                                       #as I understand it we can't distinguish
                                                       #between m for minutes and M for months.
        self.units['years']   = [ 'jahr', 'jahre',    'j' ]

        self.re_values['specials']       = 'am|dem|der|im|in|den|zum'
        self.re_values['timeseparator']  = ':'
        self.re_values['rangeseparator'] = '-'
        self.re_values['daysuffix']      = ''
        self.re_values['qunits']         = 'h|m|s|t|w|m|j'
        self.re_values['now']            = [ 'jetzt' ]

        # Used to adjust the returned date before/after the source
        #still looking for insight on how to translate all of them to german.
        self.Modifiers['from']        =  1
        self.Modifiers['before']      = -1
        self.Modifiers['after']       =  1
        self.Modifiers['vergangener'] = -1
        self.Modifiers['vorheriger']  = -1
        self.Modifiers['prev']        = -1
        self.Modifiers['letzter']     = -1
        self.Modifiers['n\xe4chster'] =  1
        self.Modifiers['dieser']      =  0
        self.Modifiers['previous']    = -1
        self.Modifiers['in a']        =  2
        self.Modifiers['end of']      =  0
        self.Modifiers['eod']         =  0
        self.Modifiers['eo']          =  0

        #morgen/abermorgen does not work, see http://code.google.com/p/parsedatetime/issues/detail?id=19
        self.dayOffsets['morgen']        =  1
        self.dayOffsets['heute']         =  0
        self.dayOffsets['gestern']       = -1
        self.dayOffsets['vorgestern']    = -2
        self.dayOffsets['\xfcbermorgen'] =  2

        # special day and/or times, i.e. lunch, noon, evening
        # each element in the dictionary is a dictionary that is used
        # to fill in any value to be replace - the current date/time will
        # already have been populated by the method buildSources
        self.re_sources['mittag']          = { 'hr': 12, 'mn': 0, 'sec': 0 }
        self.re_sources['mittags']         = { 'hr': 12, 'mn': 0, 'sec': 0 }
        self.re_sources['mittagessen']     = { 'hr': 12, 'mn': 0, 'sec': 0 }
        self.re_sources['morgen']          = { 'hr':  6, 'mn': 0, 'sec': 0 }
        self.re_sources['morgens']         = { 'hr':  6, 'mn': 0, 'sec': 0 }
        self.re_sources[r'fr\e4hst\xe4ck'] = { 'hr':  8, 'mn': 0, 'sec': 0 }
        self.re_sources['abendessen']      = { 'hr': 19, 'mn': 0, 'sec': 0 }
        self.re_sources['abend']           = { 'hr': 18, 'mn': 0, 'sec': 0 }
        self.re_sources['abends']          = { 'hr': 18, 'mn': 0, 'sec': 0 }
        self.re_sources['mitternacht']     = { 'hr':  0, 'mn': 0, 'sec': 0 }
        self.re_sources['nacht']           = { 'hr': 21, 'mn': 0, 'sec': 0 }
        self.re_sources['nachts']          = { 'hr': 21, 'mn': 0, 'sec': 0 }
        self.re_sources['heute abend']     = { 'hr': 21, 'mn': 0, 'sec': 0 }
        self.re_sources['heute nacht']     = { 'hr': 21, 'mn': 0, 'sec': 0 }
        self.re_sources['feierabend']      = { 'hr': 17, 'mn': 0, 'sec': 0 }
