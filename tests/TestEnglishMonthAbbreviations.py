import datetime
import unittest

import parsedatetime as pdt
from parsedatetime.context import pdtContext


class TestEnglishMonthAbbreviations(unittest.TestCase):
    def calendars(self):
        for locale in ('en_US', 'en_AU'):
            yield pdt.Calendar(pdt.Constants(locale, usePyICU=False))

    def test_september_dates(self):
        start = datetime.datetime(2015, 11, 1, 12).timetuple()
        expected = (2016, 9, 5, 12, 0, 0)
        accuracy = pdtContext.ACU_YEAR | pdtContext.ACU_MONTH | pdtContext.ACU_DAY
        for cal in self.calendars():
            for month in ('Sep', 'Sept', 'SEPT', 'september'):
                for source in (month + '. 5, 2016', '5 ' + month + ' 2016'):
                    with self.subTest(locale=cal.ptc.localeID, source=source):
                        result, context = cal.parse(source, start)
                        self.assertEqual(result[:6], expected)
                        self.assertEqual(context, pdtContext(accuracy))
                        result_dt, context_dt = cal.parseDT(source, start)
                        self.assertEqual(result_dt, datetime.datetime(*expected))
                        self.assertEqual(context_dt, context)

    def test_september_nlp_spans(self):
        start = datetime.datetime(2015, 11, 1, 12).timetuple()
        for cal in self.calendars():
            for phrase in ('Sept 5, 2016', '5 SEPT 2016'):
                text = 'Meet ' + phrase + ' please'
                with self.subTest(locale=cal.ptc.localeID, phrase=phrase):
                    matches = cal.nlp(text, start)
                    self.assertEqual(len(matches), 1)
                    date, context, begin, end, matched = matches[0]
                    self.assertEqual(date, datetime.datetime(2016, 9, 5, 12))
                    self.assertTrue(context.hasDate)
                    # The existing date matcher includes its leading space.
                    self.assertEqual((begin, end), (4, 5 + len(phrase)))
                    self.assertEqual(matched, ' ' + phrase)
                    self.assertEqual(text[begin:end], matched)

    def test_september_word_boundaries(self):
        for cal in self.calendars():
            for text in ('septic', 'septet', 'septum', 'asept', 'septembers'):
                with self.subTest(locale=cal.ptc.localeID, text=text):
                    self.assertIsNone(cal.nlp(text))

    def test_september_modifiers(self):
        for cal in self.calendars():
            for source_month in (1, 9, 11):
                start = datetime.datetime(2015, source_month, 1, 12).timetuple()
                for modifier in ('next', 'last', 'this'):
                    expected = cal.parse(modifier + ' September', start)
                    for month in ('Sep', 'Sept'):
                        with self.subTest(locale=cal.ptc.localeID,
                                          source_month=source_month,
                                          modifier=modifier, month=month):
                            self.assertEqual(
                                cal.parse(modifier + ' ' + month, start),
                                expected)
