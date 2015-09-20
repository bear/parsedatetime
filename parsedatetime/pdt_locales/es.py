# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base


__all__ = [
    'pdtLocale_es',
]

class pdtLocale_es(pdtLocale_base):
    """
    es Locale

    Note that I don't speak Spanish so many of the items below are still in English
    """

    def __init__(self):
        super(pdtLocale_es, self).__init__()

        self.localeID = 'es'  # don't use a unicode string
        self.dateSep = ['/']
        self.usesMeridian = False
        self.uses24 = True
        self.decimal_mark = ','

        self.Weekdays = ['lunes', 'martes', 'mi\xe9rcoles',
                         'jueves', 'viernes', 's\xe1bado', 'domingo',
                         ]
        self.shortWeekdays = ['lun', 'mar', 'mi\xe9',
                              'jue', 'vie', 's\xe1b', 'dom',
                              ]
        self.Months = ['enero', 'febrero', 'marzo',
                       'abril', 'mayo', 'junio',
                       'julio', 'agosto', 'septiembre',
                       'octubre', 'noviembre', 'diciembre'
                       ]
        self.shortMonths = ['ene', 'feb', 'mar',
                            'abr', 'may', 'jun',
                            'jul', 'ago', 'sep',
                            'oct', 'nov', 'dic'
                            ]
        self.dateFormats['full'] = "EEEE d' de 'MMMM' de 'yyyy"
        self.dateFormats['long'] = "d' de 'MMMM' de 'yyyy"
        self.dateFormats['medium'] = "dd-MMM-yy"
        self.dateFormats['short'] = "d/MM/yy"

        self.timeFormats['full'] = "HH'H'mm' 'ss z"
        self.timeFormats['long'] = "HH:mm:ss z"
        self.timeFormats['medium'] = "HH:mm:ss"
        self.timeFormats['short'] = "HH:mm"

        self.dp_order = ['d', 'm', 'y']
