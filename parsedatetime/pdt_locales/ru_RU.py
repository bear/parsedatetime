# -*- encoding: utf-8 -*-
from parsedatetime.pdt_locales import pdtLocale_base


__all__ = [
    'pdtLocale_ru',
]


class pdtLocale_ru(pdtLocale_base):
    """
    ru_RU Locale constants

    Contributed by Alexander Sapronov <sapronov.alexander92@gmail.com>
    """

    def __init__(self):
        super(pdtLocale_ru, self).__init__()

        self.localeID = 'ru_RU'
        self.dateSep = ['-', '.']
        self.timeSep = [':']
        self.meridian = []
        self.usesMeridian = False
        self.uses24 = True

        self.Weekdays = ['понедельник', 'вторник', 'среда',
                         'четверг', 'пятница', 'суббота', 'воскресенье',
                         ]
        self.shortWeekdays = ['пн', 'вт', 'ср',
                              'чт', 'пт', 'сб', 'вс',
                              ]
        # library does  not know how to conjugate words
        # библиотека не умеет спрягать слова
        self.Months = ['января', 'февраля', 'марта',
                       'апреля', 'мая', 'июня',
                       'июля', 'августа', 'сентября',
                       'октября', 'ноября', 'декабря',
                       ]
        self.shortMonths = ['явн', 'фев', 'мрт',
                            'апр', 'май', 'июн',
                            'июл', 'авг', 'сен',
                            'окт', 'нбр', 'дек',
                            ]
        self.dateFormats['full'] = 'EEEE, dd MMMM yyyy'
        self.dateFormats['long'] = 'dd MMMM yyyy'
        self.dateFormats['medium'] = 'dd-MM-yyyy'
        self.dateFormats['short'] = 'dd-MM-yy'

        self.timeFormats['full'] = 'HH:mm:ss v'
        self.timeFormats['long'] = 'HH:mm:ss z'
        self.timeFormats['medium'] = 'HH:mm:ss'
        self.timeFormats['short'] = 'HH:mm'

        self.dp_order = ['d', 'm', 'y']

        self.decimal_mark = '.'

        self.units['seconds'] = ['секунда', 'секунды', 'секунд' 'сек', 'с']
        self.units['minutes'] = ['минута', 'минуты', 'минут', 'мин', 'м']
        self.units['hours'] = ['час', 'часов', 'часа', 'ч']
        self.units['days'] = ['день', 'дней', 'д']
        self.units['weeks'] = ['неделя', 'недели', 'н']
        self.units['months'] = ['месяц', 'месяца', 'мес']
        self.units['years'] = ['год', 'года', 'годы' 'г']

        self.re_values['specials'] = 'om'
        self.re_values['timeseparator'] = ':'
        self.re_values['rangeseparator'] = '-'
        self.re_values['daysuffix'] = 'ого|ой|ий|тье'
        self.re_values['qunits'] = 'д|мес|г|ч|н|м|с'
        self.re_values['now'] = ['сейчас']

        self.Modifiers = {
            'после': 1,
            'назад': -1,
            'предыдущий': -1,
            'последний': -1,
            'далее': 1,
            'ранее': -1,
        }

        self.dayOffsets = {
            'завтра': 1,
            'сегодня': 0,
            'вчера': -1,
            'позавчера': -2,
            'послезавтра': 2,
        }

        self.re_sources = {
            'полдень': {'hr': 12, 'mn': 0, 'sec': 0},
            'день': {'hr': 13, 'mn': 0, 'sec': 0},
            'обед': {'hr': 12, 'mn': 0, 'sec': 0},
            'утро': {'hr': 6, 'mn': 0, 'sec': 0},
            'завтрак': {'hr': 8, 'mn': 0, 'sec': 0},
            'ужин': {'hr': 19, 'mn': 0, 'sec': 0},
            'вечер': {'hr': 18, 'mn': 0, 'sec': 0},
            'полночь': {'hr': 0, 'mn': 0, 'sec': 0},
            'ночь': {'hr': 21, 'mn': 0, 'sec': 0},
        }
        self.small = {
            'ноль': 0,
            'один': 1,
            'два': 2,
            'три': 3,
            'четыре': 4,
            'пять': 5,
            'шесть': 6,
            'семь': 7,
            'восемь': 8,
            'девять': 9,
            'десять': 10,
            'одинадцать': 11,
            'двенадцать': 12,
            'тринадцать': 13,
            'четырнадцать': 14,
            'пятнадцать': 15,
            'шестнадцать': 16,
            'семнадцать': 17,
            'восемнадцать': 18,
            'девятнадцать': 19,
            'двадцать': 20,
            'тридцать': 30,
            'сорок': 40,
            'пятьдесят': 50,
            'шестьдесят': 60,
            'семьдесят': 70,
            'восемьдесят': 80,
            'девяносто': 90
        }
        self.magnitude = {
            'тысяча': 1000,
            'миллион': 1000000,
            'миллиард': 1000000000,
            'триллион': 1000000000000,
            'квадриллион': 1000000000000000,
            'квинтиллион': 1000000000000000000,
            'секстиллион': 1000000000000000000000,
            'септиллион': 1000000000000000000000000,
            'октиллион': 1000000000000000000000000000,
            'нониллион': 1000000000000000000000000000000,
            'дециллион': 1000000000000000000000000000000000,
        }
