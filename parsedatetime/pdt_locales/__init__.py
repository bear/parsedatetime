# -*- encoding: utf-8 -*-

"""
pdt_locales

All of the included locale classes shipped with pdt.
"""
import os

try:
    import PyICU as pyicu
except:
    pyicu = None

import yaml


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

pdtLocales = [
    'icu',
    'en_US',
    'en_AU',
    'es_ES',
    'de_DE',
    'nl_NL',
    'ru_RU',
]


def load_yaml(path):
    """
    Read yaml data from filepath
    :param path:
    :return:
    """
    with open(path, 'r') as fio:
        return yaml.load(fio.read())


def _get_yaml_path(locale):
    """
    Return filepath of locale file
    :param locale:
    :return:
    """
    return os.path.join(os.path.dirname(__file__), '%s.yaml' % locale)


def load_locale(locale):
    """
    Return data of locale
    :param locale:
    :return:
    """
    assert locale in pdtLocales, "The locale '%s' is not supported" % locale
    _data_base = load_yaml(_get_yaml_path('base'))
    return _data_base.update(**load_yaml(_get_yaml_path(locale)))


load_locale('ru_RU')
