# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import *  # noqa

# don't use an unicode string
localeID = 'de_DE'
dateSep = ['.']
timeSep = [':']
meridian = []
usesMeridian = False
uses24 = True
decimal_mark = ','

Weekdays = [
    'montag', 'dienstag', 'mittwoch',
    'donnerstag', 'freitag', 'samstag', 'sonntag',
]
shortWeekdays = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
Months = [
    'januar', 'februar', 'märz',
    'april', 'mai', 'juni',
    'juli', 'august', 'september',
    'oktober', 'november', 'dezember',
]
shortMonths = [
    'jan', 'feb', 'mrz', 'apr', 'mai', 'jun',
    'jul', 'aug', 'sep', 'okt', 'nov', 'dez',
]

dateFormats = {
    'full': 'EEEE, d. MMMM yyyy',
    'long': 'd. MMMM yyyy',
    'medium': 'dd.MM.yyyy',
    'short': 'dd.MM.yy',
}

timeFormats = {
    'full': 'HH:mm:ss v',
    'long': 'HH:mm:ss z',
    'medium': 'HH:mm:ss',
    'short': 'HH:mm',
}

dp_order = ['d', 'm', 'y']

# the short version would be a capital M,
# as I understand it we can't distinguish
# between m for minutes and M for months.
units = {
    'seconds': ['sekunden', 'sek', 's'],
    'minutes': ['minuten', 'min'],
    'hours': ['stunden', 'std', 'h'],
    'days': ['tag', 'tage', 'tagen', 't'],
    'weeks': ['wochen', 'woche', 'w'],
    'months': ['monat', 'monate'],
    'years': ['jahren', 'jahr', 'jahre', 'j'],
}
numbers = {
    'null': 0,
    'eins': 1,
    'ein': 1,
    'zwei': 2,
    'drei': 3,
    'vier': 4,
    'fünf': 5,
    'funf': 5,
    'sechs': 6,
    'sieben': 7,
    'acht': 8,
    'neun': 9,
    'zehn': 10,
    'elf': 11,
    'zwölf':12,
    'zwolf': 12,
    'zwanzig': 20,
    'dreißig': 30,
    'dreibig': 30,
    'vierzig': 40,
    'fünfzig': 50,
    'funfzig': 50,
    'sechzig': 60,
    'siebzig': 70,
    'achtzig': 80,
    'neunzig': 90,
    'hundert': 100,
    'ignore': 'und'

}
re_values = re_values.copy()
re_values.update({
    'specials': 'am|dem|der|im|in|den|zum',
    'timeseparator': ':',
    'of': '.', # "eg. 3rd of march"
    'rangeseparator': '-|bis',
    'daysuffix': '',
    'qunits': 'h|m|s|t|w|m|j',
    'now': ['jetzt'],
    'after': 'nach|vor', # imply after/later/ago but at the beginning of a phrase
    'ago': 'später|spater', # imply after/later/ago but at the end of a phrase
    'from': 'von',  # num unit from rel
    'this': 'deises|diesen|kommenden',
    'next': 'nächsten|nächster|nächste|nachsten|nachster|nachste',
    'last': 'letzter|letzten|letzte',
    'in': r'in',  # "in 5 days" #done (german same eng)
    'since': 'seit',  # since time, since date, since num unit
})

# Used to adjust the returned date before/after the source
# still looking for insight on how to translate all of them to german.
Modifiers = {
    'from': 1,
    'before': -1,

    'nach': 1,
    'vor': -1,
    'später': -1,
    'spater': -1,

    'vergangener': -1,
    'vorheriger': -1,

    'prev': -1,

    'letzter': -1,
    'letzten': -1,
    'letzte': -1,

    'nächster': 1,
    'nächsten': 1,
    'nächste': 1,
    'nachster': 1,
    'nachsten': 1,
    'nachste': 1,

    'dieser': 0,
    'diesen': 0,
    'kommenden': 0,

    'previous': -1,
    'in a': 2,
    'end of': 0,
    'eod': 0,
    'eo': 0,
}

# morgen/abermorgen does not work, see
# http://code.google.com/p/parsedatetime/issues/detail?id=19
dayOffsets = {
    'morgen': 1,
    'heute': 0,
    'gestern': -1,
    'vorgestern': -2,
    'übermorgen': 2,
    'ubermorgen': 2,
}

# special day and/or times, i.e. lunch, noon, evening
# each element in the dictionary is a dictionary that is used
# to fill in any value to be replace - the current date/time will
# already have been populated by the method buildSources
re_sources = {
    'mittag': {'hr': 12, 'mn': 0, 'sec': 0},
    'mittags': {'hr': 12, 'mn': 0, 'sec': 0},
    'mittagessen': {'hr': 12, 'mn': 0, 'sec': 0},
    'morgen': {'hr': 6, 'mn': 0, 'sec': 0},
    'morgens': {'hr': 6, 'mn': 0, 'sec': 0},
    'frühstück': {'hr': 8, 'mn': 0, 'sec': 0},
    'abendessen': {'hr': 19, 'mn': 0, 'sec': 0},
    'abend': {'hr': 18, 'mn': 0, 'sec': 0},
    'abends': {'hr': 18, 'mn': 0, 'sec': 0},
    'mitternacht': {'hr': 0, 'mn': 0, 'sec': 0},
    'nacht': {'hr': 21, 'mn': 0, 'sec': 0},
    'nachts': {'hr': 21, 'mn': 0, 'sec': 0},
    'heute abend': {'hr': 21, 'mn': 0, 'sec': 0},
    'heute nacht': {'hr': 21, 'mn': 0, 'sec': 0},
    'feierabend': {'hr': 17, 'mn': 0, 'sec': 0},
}
