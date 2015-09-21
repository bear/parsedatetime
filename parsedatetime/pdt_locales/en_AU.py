# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base


__all__ = [
    'pdtLocale_au',
]

class pdtLocale_au(pdtLocale_base):
    """
    en_AU Locale
    """
    def __init__(self):
        super( pdtLocale_au, self ).__init__()

        self.localeID = 'en_AU'   # don't use a unicode string
        self.dateSep  = [ '-', '/' ]
        self.uses24   = False

        self.dateFormats['full']   = 'EEEE, d MMMM yyyy'
        self.dateFormats['long']   = 'd MMMM yyyy'
        self.dateFormats['medium'] = 'dd/MM/yyyy'
        self.dateFormats['short']  = 'd/MM/yy'

        self.timeFormats['long']   = self.timeFormats['full']

        self.dp_order = [ 'd', 'm', 'y' ]
