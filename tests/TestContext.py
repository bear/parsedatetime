# -*- coding: utf-8 -*-
"""
Test pdtContext
"""

import sys
import time
import parsedatetime as pdt
from parsedatetime.context import pdtContext

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class test(unittest.TestCase):

    def setUp(self):
        self.cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
        (self.yr, self.mth, self.dy, self.hr, self.mn,
         self.sec, self.wd, self.yd, self.isdst) = time.localtime()

    def testContext(self):
        self.assertEqual(self.cal.parse('5 min from now')[1],
                         pdtContext(pdtContext.ACU_MIN | pdtContext.ACU_NOW))
        self.assertEqual(self.cal.parse('5 min from now',
                                        version=pdt.VERSION_FLAG_STYLE)[1], 2)
        self.assertEqual(self.cal.parse('7/11/2015')[1],
                         pdtContext(pdtContext.ACU_YEAR |
                                    pdtContext.ACU_MONTH | pdtContext.ACU_DAY))
        self.assertEqual(self.cal.parse('7/11/2015',
                                        version=pdt.VERSION_FLAG_STYLE)[1], 1)
        self.assertEqual(self.cal.parse('14/32/2015')[1],
                         pdtContext(0))
        self.assertEqual(self.cal.parse('25:23')[1],
                         pdtContext())

    def testSources(self):
        self.assertEqual(self.cal.parse('afternoon 5pm')[1],
                         pdtContext(pdtContext.ACU_HALFDAY |
                                    pdtContext.ACU_HOUR))

        self.assertEqual(self.cal.parse('morning')[1],
                         pdtContext(pdtContext.ACU_HALFDAY))

        self.assertEqual(self.cal.parse('night', version=1)[1], 2)

    def testThreadRun(self):
        from threading import Thread
        t = Thread(target=lambda: self.cal.evalRanges('4p-6p'))
        # should not throw out AttributeError
        t.start()


if __name__ == "__main__":
    unittest.main()
