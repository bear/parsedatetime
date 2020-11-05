# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import *  # noqa

# don't use an unicode string
localeID = 'pt_BR'
dateSep = ['/']
usesMeridian = False
uses24 = True
decimal_mark = ','

Weekdays = [
    'segunda|segunda-feira', 'terça|terça-feira', 'quarta|quarta-feira',
    'quinta|quinta-feira', 'sexta|sexta-feira', 'sábado', 'domingo',
]
shortWeekdays = [
    'seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom',
]
Months = [
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
    'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
]
shortMonths = [
    'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez'
]
dateFormats = {
    'full': "EEEE, d' de 'MMMM' de 'yyyy",
    'long': "d' de 'MMMM' de 'yyyy",
    'medium': "dd-MM-yy",
    'short': "dd/MM/yyyy",
}

timeFormats = {
    'full': "HH'H'mm' 'ss z",
    'long': "HH:mm:ss z",
    'medium': "HH:mm:ss",
    'short': "HH:mm",
}

dp_order = ['d', 'm', 'y']

numbers = {
    'zero': 0,
    'um': 1,
    'um(a)': 1,
    'um(a)': 1,
    'dois': 2,
    'três': 3,
    'quatro': 4,
    'cinco': 5,
    'seis': 6,
    'sete': 7,
    'oito': 8,
    'nove': 9,
    'dez': 10,
    'onze': 11,
    'treze': 13,
    'quatorze': 14,
    'quinze': 15,
    'dezesseis': 16,
    'dezessete': 17,
    'dezoito': 18,
    'dezenove': 19,
    'vinte': 20,
}

units = {
    'seconds': ['segundo', 'seg', 's'],
    'minutes': ['minuto', 'min', 'm'],
    'days': ['dia', 'dias', 'd'],
    'months': ['mês', 'meses'],
}

Modifiers = {
    'de': 1,
    'antes': -1,
    'depois': 1,
    'atrás': -1,
    'anterior': -1,
    'anterior': -1,
    'último': -1,
    'próximo': 1,
    'anterior': -1,
    'fim do': 0,
    'esta': 0,
    'fim do dia': 1,
    'fim do mês': 1,
    'fim do ano': 1,
}

dayOffsets = {
    'amanhã': 1,
    'hoje': 0,
    'ontem': -1,
}

re_sources = {
    'meio dia': {'hr': 12, 'mn': 0, 'sec': 0},
    'tarde': {'hr': 13, 'mn': 0, 'sec': 0},
    'almoço': {'hr': 12, 'mn': 0, 'sec': 0},
    'manhã': {'hr': 6, 'mn': 0, 'sec': 0},
    'café da manhã': {'hr': 8, 'mn': 0, 'sec': 0},
    'jantar': {'hr': 19, 'mn': 0, 'sec': 0},
    'tarde': {'hr': 18, 'mn': 0, 'sec': 0},
    'meia noite': {'hr': 0, 'mn': 0, 'sec': 0},
    'noite': {'hr': 21, 'mn': 0, 'sec': 0},
    'esta noite': {'hr': 21, 'mn': 0, 'sec': 0},
    'final do dia': {'hr': 17, 'mn': 0, 'sec': 0},
}

small = {
    'zero': 0,
    'um': 1,
    'um(a)': 1,
    'um(a)': 1,
    'dois': 2,
    'três': 3,
    'quatro': 4,
    'cinco': 5,
    'seis': 6,
    'sete': 7,
    'oito': 8,
    'nove': 9,
    'dez': 10,
    'onze': 11,
    'doze': 12,
    'treze': 13,
    'quatorze': 14,
    'quinze': 15,
    'dezesseis': 16,
    'dezessete': 17,
    'dezoito': 18,
    'dezenove': 19,
    'vinte': 20,
    'trinta': 30,
    'quarenta': 40,
    'cinquenta': 50,
    'sessenta': 60,
    'setenta': 70,
    'oitenta': 80,
    'noventa': 90
}

magnitude = {
    'mil': 1000,
    'milhão': 1000000,
    'bilhão': 1000000000,
    'trilhão': 1000000000000,
    'quadrilhão': 1000000000000000,
    'quintilhão': 1000000000000000000,
    'sextilhão': 1000000000000000000000,
    'septilhão': 1000000000000000000000000,
    'octilhão': 1000000000000000000000000000,
    'nonilhão': 1000000000000000000000000000000,
    'decilhão': 1000000000000000000000000000000000,
}