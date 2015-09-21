# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base

__all__ = [
    'pdtLocale_ptBR',
]

class pdtLocale_ptBR(pdtLocale_base):
    """
    pt_BR Locale

    """
    def __init__(self):
        super( pdtLocale_ptBR, self ).__init__()

        self.localeID     = 'pt_BR'   # don't use a unicode string
        self.dateSep      = [ '/' ]
        self.usesMeridian = False
        self.uses24       = True
        self.decimal_mark = ','

        self.Weekdays      = [ 'segunda-feira', 'ter\xe7a-feira', 'quarta-feira',
                               'quinta-feira', 'sexta-feira', 's\xe1bado', 'domingo',
                             ]
        self.shortWeekdays = [ 'seg', 'ter', 'qua',
                               'qui', 'sex', 's\xe1b', 'dom',
                             ]
        self.Months        = [ 'janeiro', 'fevereiro', 'mar\xe7o',
                               'abril', 'maio', 'junho',
                               'julho', 'agosto', 'setembro',
                               'outubro', 'novembro', 'dezembro'
                             ]
        self.shortMonths   = [ 'jan', 'fev', 'mar',
                               'abr', 'mai', 'jun',
                               'jul', 'ago', 'set',
                               'out', 'nov', 'dez'
                             ]
        self.dateFormats['full']   = "EEEE, d' de 'MMMM' de 'yyyy"
        self.dateFormats['long']   = "d' de 'MMMM' de 'yyyy"
        self.dateFormats['medium'] = "dd-MM-yy"
        self.dateFormats['short']  = "dd/MM/yyyy"

        self.timeFormats['full']   = "HH'H'mm' 'ss z"
        self.timeFormats['long']   = "HH:mm:ss z"
        self.timeFormats['medium'] = "HH:mm:ss"
        self.timeFormats['short']  = "HH:mm"

        self.dp_order = [ 'd', 'm', 'y' ]

        self.units['seconds'] = [ 'segundo', 'seg', 's']
        self.units['minutes'] = [ 'minuto', 'min',  'm']
        self.units['days']    = [ 'dia',  'dias',   'd']
        self.units['months']  = [ 'm\xeas',     'meses']

