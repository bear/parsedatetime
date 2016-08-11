# -*- coding: utf-8 -*-
"""
Test parsing of strings that are phrases
"""
from __future__ import unicode_literals

import sys
import time
import datetime
import parsedatetime as pdt
from . import utils

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class test(unittest.TestCase):

    # a special compare function for nlp returned data

    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, dateOnly=False):
        target = result
        value = check

        if target is None and value is None:
            return True

        if (target is None and value is not None) or \
                (target is not None and value is None):
            return False

        if len(target) != len(value):
            return False

        for i in range(0, len(target)):
            target_date = target[i][0]
            value_date = value[i][0]

            if target_date.year != value_date.year or \
                    target_date.month != value_date.month or \
                    target_date.day != value_date.day or \
                    target_date.hour != value_date.hour or \
                    target_date.minute != value_date.minute:
                return False
            if target[i][1] != value[i][1]:
                return False
            if target[i][2] != value[i][2]:
                return False
            if target[i][3] != value[i][3]:
                return False
            if target[i][4] != value[i][4]:
                return False

        return True

    def setUp(self):
        self.cal = pdt.Calendar()
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testLongPhrase(self):
        # note: these tests do not need to be as dynamic as the others because
        #       this is still based on the parse() function, so all tests of
        #       the actual processing of the datetime value returned are
        #       applicable to this. Here we are concerned with ensuring the
        #       correct portions of text and their positions are extracted and
        #       processed.
        start = datetime.datetime(2013, 8, 1, 21, 25, 0).timetuple()
        target = ((datetime.datetime(2013, 8, 5, 20, 0),
                   3, 17, 37, 'At 8PM on August 5th'),
                  (datetime.datetime(2013, 8, 9, 21, 0),
                   3, 72, 90, 'next Friday at 9PM'),
                  (datetime.datetime(2013, 8, 1, 21, 30, 0),
                   2, 120, 132, 'in 5 minutes'),
                  (datetime.datetime(2013, 8, 8, 9, 0),
                   1, 173, 182, 'next week'))

        # positive testing
        self.assertExpectedResult(self.cal.nlp(
            "I'm so excited!! At 8PM on August 5th i'm going to fly to "
            "Florida. Then next Friday at 9PM i'm going to Dog n Bone! "
            "And in 5 minutes I'm going to eat some food! Talk to you "
            "next week.", start), target)

        target = datetime.datetime(
            self.yr, self.mth, self.dy, 17, 0, 0).timetuple()

    def testQuotes(self):
        # quotes should not interfere with datetime language recognition
        start = datetime.datetime(2013, 8, 1, 21, 25, 0).timetuple()
        target = self.cal.nlp(
            "I'm so excited!! At '8PM on August 5th' i'm going to fly to "
            "Florida. Then 'next Friday at 9PM' i'm going to Dog n Bone! "
            "And in '5 minutes' I'm going to eat some food! Talk to you "
            '"next week"', start)

        self.assertEqual(target[0][4], "At '8PM on August 5th")
        self.assertEqual(target[1][4], "next Friday at 9PM")
        self.assertEqual(target[2][4], "in '5 minutes")
        self.assertEqual(target[3][4], "next week")

    def testPrefixes(self):
        # nlp has special handling for on/in/at prefixes
        start = datetime.datetime(2013, 8, 1, 21, 25, 0).timetuple()

        target = self.cal.nlp("Buy a balloon on Monday", start)
        self.assertEqual(target[0][4], "on Monday")

        target = self.cal.nlp("Buy a balloon at noon", start)
        self.assertEqual(target[0][4], "at noon")

        target = self.cal.nlp("Buy a balloon in a month", start)
        self.assertEqual(target[0][4], "in a month")

        # Should no longer pull "on" off the end of balloon
        target = self.cal.nlp("Buy a balloon Monday", start)
        self.assertEqual(target[0][4], "Monday")

    def testFalsePositives(self):
        # negative testing - no matches should return None
        start = datetime.datetime(2013, 8, 1, 21, 25, 0).timetuple()
        self.assertExpectedResult(self.cal.nlp(
            "Next, I'm so excited!! So many things that are going to "
            "happen every week!!", start), None)
        self.assertExpectedResult(self.cal.nlp("$300", start), None)
        self.assertExpectedResult(self.cal.nlp("300ml", start), None)
        self.assertExpectedResult(self.cal.nlp("nice ass", start), None)
