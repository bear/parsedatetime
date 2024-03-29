# -*- coding: utf-8 -*-
import sys
import time
import datetime
import unittest
import parsedatetime as pdt
from parsedatetime.pdt_locales import get_icu
from parsedatetime.context import pdtContext
from . import utils


pdtLocale_en = get_icu('en_US')
pdtLocale_en.Weekdays = [
    'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday', 'sunday']

pdtLocale_en.shortWeekdays = [
    'mon|mond', 'tue|tues', 'wed|wedn',
    'thu|thur|thurs', 'fri|frid', 'sat|sa', 'sun|su']

pdtLocale_en.Months = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december']

pdtLocale_en.shortMonths = [
    'jan|janu', 'feb|febr', 'mar|marc', 'apr|apri', 'may', 'jun|june',
    'jul', 'aug|augu', 'sep|sept', 'oct|octo', 'nov|novem', 'dec|decem']


class test(unittest.TestCase):

    @utils.assertEqualWithComparator
    def assertExpectedResult(self, result, check, **kwargs):
        return utils.compareResultByTimeTuplesAndFlags(result, check, **kwargs)

    def setUp(self):
        pdt.pdtLocales['en_us'] = pdtLocale_en  # override for the test
        self.ptc = pdt.Constants('en_us', usePyICU=False)
        self.cal = pdt.Calendar(self.ptc)
        (self.yr, self.mth, self.dy, self.hr,
         self.mn, self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testDaysOfWeek(self):
        start = datetime.datetime(
            2014, 10, 25, self.hr, self.mn, self.sec).timetuple()

        target = datetime.datetime(
            2014, 10, 26, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(self.cal.parse('sunday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('sun', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('su', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 10, 27, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(self.cal.parse('Monday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('mon', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('mond', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 10, 28, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('tuesday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('tues', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('tue', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 10, 29, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('wednesday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('wedn', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('wed', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 10, 30, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('thursday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('thu', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('thur', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('thurs', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 10, 31, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(self.cal.parse('friday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('fri', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('frid', start), (target, pdtContext(pdtContext.ACU_DAY)))

        target = datetime.datetime(
            2014, 11, 1, self.hr, self.mn, self.sec).timetuple()
        self.assertExpectedResult(
            self.cal.parse('saturday', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('sat', start), (target, pdtContext(pdtContext.ACU_DAY)))
        self.assertExpectedResult(self.cal.parse('sa', start), (target, pdtContext(pdtContext.ACU_DAY)))

    def testMonths(self):
        start = datetime.datetime(
            2014, 1, 1, self.hr, self.mn, self.sec).timetuple()
        for dates, expected_date in [
            ('jan|janu|january', datetime.datetime(
                2014, 1, 1, self.hr, self.mn, self.sec).timetuple()),
            ('feb|febr|february', datetime.datetime(
                2014, 2, 1, self.hr, self.mn, self.sec).timetuple()),
            ('mar|marc|march', datetime.datetime(
                2014, 3, 1, self.hr, self.mn, self.sec).timetuple()),
            ('apr|apri|april', datetime.datetime(
                2014, 4, 1, self.hr, self.mn, self.sec).timetuple()),
            ('may|may', datetime.datetime(
                2014, 5, 1, self.hr, self.mn, self.sec).timetuple()),
            ('jun|june', datetime.datetime(
                2014, 6, 1, self.hr, self.mn, self.sec).timetuple()),
            ('jul|july', datetime.datetime(
                2014, 7, 1, self.hr, self.mn, self.sec).timetuple()),
            ('aug|augu|august', datetime.datetime(
                2014, 8, 1, self.hr, self.mn, self.sec).timetuple()),
            ('sep|sept|september', datetime.datetime(
                2014, 9, 1, self.hr, self.mn, self.sec).timetuple()),
            ('oct|octo|october', datetime.datetime(
                2014, 10, 1, self.hr, self.mn, self.sec).timetuple()),
            ('nov|novem|november', datetime.datetime(
                2014, 11, 1, self.hr, self.mn, self.sec).timetuple()),
            ('dec|decem|december', datetime.datetime(
                2014, 12, 1, self.hr, self.mn, self.sec).timetuple())
        ]:
            for dateText in dates.split("|"):
                # print dateText
                self.assertExpectedResult(
                    self.cal.parse(dateText, start), (expected_date, pdtContext(pdtContext.ACU_MONTH)))
