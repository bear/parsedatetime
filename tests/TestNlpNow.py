import datetime
import unittest

import parsedatetime as pdt
from parsedatetime.context import pdtContext


class TestNlpNow(unittest.TestCase):
    def setUp(self):
        self.cal = pdt.Calendar(pdt.Constants(localeID='en_US', usePyICU=False))
        self.source = datetime.datetime(2013, 8, 1, 21, 25, 0)

    def testRelativeNow(self):
        cases = (
            ('1 year from now', datetime.datetime(2014, 8, 1, 21, 25),
             pdtContext.ACU_YEAR | pdtContext.ACU_NOW),
            ('one year from now', datetime.datetime(2014, 8, 1, 21, 25),
             pdtContext.ACU_YEAR | pdtContext.ACU_NOW),
            ('5 minutes from now', datetime.datetime(2013, 8, 1, 21, 30),
             pdtContext.ACU_MIN | pdtContext.ACU_NOW),
            ('5 minutes before now', datetime.datetime(2013, 8, 1, 21, 20),
             pdtContext.ACU_MIN | pdtContext.ACU_NOW),
        )
        for phrase, expected, accuracy in cases:
            with self.subTest(phrase=phrase):
                text = 'Remind me ' + phrase + ', please.'
                result = self.cal.nlp(text, self.source.timetuple())
                self.assertEqual(result, ((expected, pdtContext(accuracy),
                                          10, 10 + len(phrase), phrase),))
                self.assertEqual(text[:result[0][2]] + text[result[0][3]:],
                                 'Remind me , please.')

    def testStandaloneNow(self):
        for phrase in ('now', 'right now', 'RIGHT NOW'):
            with self.subTest(phrase=phrase):
                result = self.cal.nlp(phrase, self.source.timetuple())
                self.assertEqual(result, ((self.source,
                                          pdtContext(pdtContext.ACU_NOW),
                                          0, len(phrase), phrase),))

    def testLocalizedNow(self):
        cal = pdt.Calendar(pdt.Constants(localeID='fr_FR', usePyICU=False))
        result = cal.nlp('maintenant', self.source.timetuple())
        self.assertEqual(result, ((self.source, pdtContext(pdtContext.ACU_NOW),
                                  0, 10, 'maintenant'),))

    def testWordBoundaries(self):
        self.assertIsNone(self.cal.nlp('unknown nowhere snow',
                                       self.source.timetuple()))

    def testNegativeQuantityAfterNow(self):
        for phrase in ('-5 minutes from now', '-5m from now'):
            with self.subTest(phrase=phrase):
                result = self.cal.nlp('now; ' + phrase,
                                      self.source.timetuple())
                self.assertEqual(result, (
                    (self.source, pdtContext(pdtContext.ACU_NOW), 0, 3, 'now'),
                    (self.source - datetime.timedelta(minutes=5),
                     pdtContext(pdtContext.ACU_MIN | pdtContext.ACU_NOW),
                     5, 5 + len(phrase), phrase),
                ))

    def testNowDoesNotConsumePrefixes(self):
        for text, phrase in (('Log in now', 'now'),
                             ('Come in right now.', 'right now'),
                             ('Act at RIGHT NOW', 'RIGHT NOW')):
            with self.subTest(text=text):
                start = text.index(phrase)
                result = self.cal.nlp(text, self.source.timetuple())
                self.assertEqual(result, ((self.source,
                                          pdtContext(pdtContext.ACU_NOW),
                                          start, start + len(phrase), phrase),))
