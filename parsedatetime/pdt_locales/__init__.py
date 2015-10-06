# -*- encoding: utf-8 -*-

"""
pdt_locales

All of the included locale classes shipped with pdt.
"""

from __future__ import absolute_import
import os

import yaml

from .icu import get_icu

locale_extension = '.yaml'
locales = [
    'icu',
]

locales.extend(
    map(lambda x: x.split(locale_extension)[0],
        filter(lambda x: locale_extension in x, os.listdir(os.path.dirname(__file__)))))


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


def load_locale(locale, icu=False):
    """
    Return data of locale
    :param locale:
    :return:
    """
    assert locale in locales, "The locale '%s' is not supported" % locale
    result = load_yaml(_get_yaml_path('base'))
    if icu:
        result.update(**get_icu(locale))
    else:
        result.update(**load_yaml(_get_yaml_path(locale)))
    return result

# _ = load_locale('en_US', icu=True)
# print(_)
# print(pdtLocale_icu('en_US').icu)
