# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import *  # noqa

# don't use an unicode string
localeID = 'es'
dateSep = ['/', '-']
meridian = []
usesMeridian = False
uses24 = True
decimal_mark = ','

Weekdays = [
    'lunes', 'martes', 'miércoles',
    'jueves', 'viernes', 'sábado', 'domingo',
]
shortWeekdays = [
    'lun|l', 'mar|m', 'mié|x',
    'jue|j', 'vie|v', 'sáb|s', 'dom|d',
]
Months = [
    'enero', 'febrero', 'marzo',
    'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre',
    'octubre', 'noviembre', 'diciembre',
]
shortMonths = [
    'ene', 'feb', 'mar',
    'abr', 'may', 'jun',
    'jul', 'ago', 'sep',
    'oct', 'nov', 'dic',
]
dateFormats = {
    'full': "EEEE d' de 'MMMM' de 'yyyy",
    'long': "d' de 'MMMM' de 'yyyy",
    'medium': "dd-MMM-yy",
    'short': "d/MM/yy",
}

timeFormats = {
    'full': "HH'H'mm' 'ss z",
    'long': "HH:mm:ss z",
    'medium': "HH:mm:ss",
    'short': "HH:mm",
}

dp_order = ['d', 'm', 'y']

numbers = {
    'cero': 0,
    'uno': 1,
    'dos': 2,
    'tres': 3,
    'cuatro': 4,
    'cinco': 5,
    'seis': 6,
    'siete': 7,
    'ocho': 8,
    'neuve': 9,
    'diez': 10,
    'dieci': 10, # for 17-19
    'dieciséis': 16,
    'onze': 11,
    'doce': 12,
    'trece': 13,
    'catorce': 14,
    'quince': 15,
    'veinte': 20,
    'veinti': 20, # for 21-29
    'veintidós': 22,
    'veintitrés': 23,
    'veintiséis': 26,
    'thirt': 30,
    'treinta': 30,
    'cuarenta': 40,
    'cincuenta': 50,
    'sesenta': 60,
    'setenta': 70,
    'ochenta': 80,
    'noventa': 90,
    'cien': 100,
    'ciento': 100,
    'cientos': 100,
    'quinientos': 500,
    'setecientos': 700,
    'novecientos': 900,
}

decimal_mark = ','

# this will be added to re_values later
units = {
    'seconds': ['segundo', 'seguendos', 's'],
    'minutes': ['minuto', 'minutos', 'min'],
    'hours': ['hora', ' horas','h'],
    'days': ['día', 'días', 'dia', 'dias', 'd'],
    'weeks': ['semana', 'semanas'],
    'months': ['mes'],
    'years': ['año', 'ano'],
}

# text constants to be used by later regular expressions
re_values = {
    'specials': 'la|las|en|es|son',
    'timeseparator': '(?:\:|h|\s*horas?\s*)',
    'of': 'de', # "eg. 3rd of march"
    'rangeseparator': '-|a',
    'daysuffix': '.°|.ª',
    'meridian': r'am|pm|a\.m\.|p\.m\.|a|p',
    'qunits': 'h|s|d',
    'now': ['ahora', 'ahora mismo', 'inmediatamente'],
    'after': r'después\sde|despues\sde|hace|después|despues', # imply after/later/ago but at the beginning of a phrase
    'ago': 'después|despues', # imply after/later/ago but at the end of a phrase
    'from' : r'a\spartir\sde|de|desde\sel|desde|antes|antes\sde', # num unit from rel
    'this': 'este|esta|esto|viene|venidera|venidero|venideras|venideros|viniendo',
    'next': 'próximo|próximos|proximo|proximos|próxima|próximas|proxima|proximas|siguiente|siguientes',
    'last':'pasado|pasados|pasada|pasadas',
    'in': 'en', # "in 5 days"
    'since': r'desde|desde\sel|desde\slas|desde\sla|desde\sel' # since time, since date, since num unit

}

# Used to adjust the returned date before/after the source
Modifiers = {
    'antes': -1,
    'anterior': -1,
    'después de': 1,
    'despues de': 1,
    'hace':-1,
    'previo': -1,
    'desde': -1,
    'desde el': -1,
    'desde la': -1,
    'desde las': -1,
    'desde en': -1,
    'último': -1,
    'ultimo': -1,
    'pasado': -1,
    'pasados': -1,
    'pasada':-1,
    'pasadas': -1,
    'fin de': 0,
    'esta': 0,
    'esto': 0,
    'este': 0,
    'venir': 0,
    'viene': 0,
    'venidera': 0,
    'viniendo': 0,
    'próximo': 1,
    'proximo': 1,
    'más tarde': 1,
    'mas tarde': 1,
    'siguiente': 1,
    'eod': 1,
    'fin del día': 1,
    'fin del dia'
    'eom': 1,
    'fin de mes': 1,
    'eoy': 1,
    'fin de año': 1,
}

dayOffsets = {
    'pasado mañana': 2,
    'pasado manana': 2,
    'mañana': 1,
    'manana': 1,
    'hoy': 0,
    'ayer': -1,
    'anteayer': -2,
}

# special day and/or times, i.e. lunch, noon, evening
# each element in the dictionary is a dictionary that is used
# to fill in any value to be replace - the current date/time will
# already have been populated by the method buildSources
re_sources = {
    'noon': {'hr': 12, 'mn': 0, 'sec': 0},
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

small = {
    'cero': 0,
    'uno': 1,
    'dos': 2,
    'tres': 3,
    'cuatro': 4,
    'cinco': 5,
    'seis': 6,
    'siete': 7,
    'ocho': 8,
    'neuve': 9,
    'diez': 10,
    'onze': 11,
    'doce': 12,
    'trece': 13,
    'catorce': 14,
    'quince': 15,
    'dieciséis': 16,
    'dieciseis': 16,
    'diecisiete': 17,
    'dieciocho': 18,
    'diecinueve': 19,
    'veinte': 20,
    'veintiuno': 21,
    'veintidós': 21,
    'veintidos': 22,
    'vingt-deux': 22,
    'veintitrés': 23,
    'veintitres': 23,
    'veinticuatro': 24,
    'trienta': 30,
    'treinta y seis': 36,
    'cuarenta': 40,
    'cuarenta y cuatro': 48,
    'cincuenta': 50,
    'sesenta': 60,
    'setenta': 70,
    'ochenta': 80,
    'noventa': 90,
    'cien': 100,
}

magnitude = {
    'mil': 1000,
    'millione': 1000000,
    'milliones': 1000000,

    'milliard': 1000000000,
    'trillion': 1000000000000,
    'quadrillion': 1000000000000000,
    'quintillion': 1000000000000000000,
    'sextillion': 1000000000000000000000,
    'septillion': 1000000000000000000000000,
    'octillion': 1000000000000000000000000000,
    'nonillion': 1000000000000000000000000000000,
    'décillion': 1000000000000000000000000000000000,
    'decillion': 1000000000000000000000000000000000,
}

ignore = ()
