
"""
Test parsing of strings that are phrases with the
ptc.StartTimeFromSourceTime flag set to True
"""

import unittest, time, datetime
import parsedatetime as pdt

  # a special compare function is used to allow us to ignore the seconds as
  # the running of the test could cross a minute boundary
def _compareResults(result, check, dateOnly=False, debug=False):
    target, t_flag = result
    value,  v_flag = check

    t_yr, t_mth, t_dy, t_hr, t_min, _, _, _, _ = target
    v_yr, v_mth, v_dy, v_hr, v_min, _, _, _, _ = value

    if dateOnly:
        return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy)) and (t_flag == v_flag)
    else:
        return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy) and
                (t_hr == v_hr) and (t_min == v_min)) and (t_flag == v_flag)


class test(unittest.TestCase):

    def setUp(self):
        self.cal = pdt.Calendar()
        self.cal.ptc.StartTimeFromSourceTime = True
        self.yr, self.mth, self.dy, self.hr, self.mn, self.sec, self.wd, self.yd, self.isdst = time.localtime()

    def testEndOfPhrases(self):
        s = datetime.datetime.now()

          # find out what month we are currently on
          # set the day to 1 and then go back a day
          # to get the end of the current month
        (yr, mth, dy, hr, mn, sec, _, _, _) = s.timetuple()

        m    = mth
        mth += 1
        if mth > 12:
            mth = 1
            yr += 1

        s = datetime.datetime(yr,   m, dy, 13, 14, 15)
        t = datetime.datetime(yr, mth,  1, 13, 14, 15) + datetime.timedelta(days=-1)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('eom',         start), (target, 2)))
        self.assertTrue(_compareResults(self.cal.parse('meeting eom', start), (target, 2)))

        s = datetime.datetime.now()

        (yr, mth, dy, hr, mn, sec, wd, yd, isdst) = s.timetuple()

        s = datetime.datetime(yr, mth,  1, 13, 14, 15)
        t = datetime.datetime(yr,  12, 31, 13, 14, 15)

        start  = s.timetuple()
        target = t.timetuple()

        self.assertTrue(_compareResults(self.cal.parse('eoy',         start), (target, 2)))
        self.assertTrue(_compareResults(self.cal.parse('meeting eoy', start), (target, 2)))
