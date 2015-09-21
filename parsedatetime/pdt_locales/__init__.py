# -*- encoding: utf-8 -*-

"""
pdt_locales

All of the included locale classes shipped with pdt.
"""

try:
    import PyICU as pyicu
except:
    pyicu = None


def lcase(x):
    return x.lower()


from .base import pdtLocale_base, pdtLocale_icu

from .de_DE import *
from .en_AU import *
from .en_US import *
from .es import *
from .nl_NL import *
from .pt_BR import *
from .ru_RU import *
