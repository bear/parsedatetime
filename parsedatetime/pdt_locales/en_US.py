# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base


__all__ = [
    'pdtLocale_en',
]

class pdtLocale_en(pdtLocale_base):
    """
    en_US Locale
    """
    def __init__(self):
        super( pdtLocale_en, self ).__init__()

        self.localeID = 'en_US'  # don't use a unicode string
        self.uses24   = False


