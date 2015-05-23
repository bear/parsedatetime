
"""
Unit tests for parsedatetime

The tests can be run as a C{suite} by running::

    python run_tests.py parsedatetime

Requires Python 3.0 or later
"""

__author__       = 'Mike Taylor (bear@code-bear.com)'
__copyright__    = 'Copyright (c) 2004 Mike Taylor'
__license__      = 'Apache v2.0'
__version__      = '1.0.0'
__contributors__ = [ 'Darshana Chhajed',
                     'Michael Lim (lim.ck.michael@gmail.com)',
                     'Bernd Zeimetz (bzed@debian.org)',
                   ]
import logging

log = logging.getLogger('parsedatetime')
echoHandler   = logging.StreamHandler()
echoFormatter = logging.Formatter('%(levelname)-8s %(message)s')
log.addHandler(echoHandler)

#log.setLevel(logging.DEBUG)     

def assertEqualWithComparator(comparator):
    """
    Fail a little less cryptically that unittest.assertTrue when comparing a
    result against a target value. Shows the result and the target in the
    failure message.
    """
    def decoratedComparator(self, result, check, **kwargs):
        equal = comparator(self, result, check, **kwargs)
        failureMessage = 'Result does not match target value\n\n\tResult:\n\t%s\n\n\tExpected:\n\t%s'

        if not equal:
            self.fail(failureMessage % (result, check))

    return decoratedComparator

def compareResultByTimeTuplesAndFlags(result, check, dateOnly=False):
    """
    Ensures that flags are an exact match and time tuples a close match when
    given data in the format ((timetuple), flag)
    """
    return _compareTimeTuples(result[0], check[0], dateOnly) and _compareFlags(result[1], check[1])

def compareResultByFlags(result, check, dateOnly=False):
    """
    Ensures that flags are an exact match when given data in the format
    ((timetuple), flag)
    """
    return _compareFlags(result[1], check[1])

def compareResultByTimeTupleRangesAndFlags(result, check, dateOnly=False):
    """
    Ensures that flags are an exact match and time tuples a close match when
    given data in the format ((timetuple), (timetuple), flag)
    """
    return _compareTimeTuples(result[0], check[0], dateOnly) and _compareTimeTuples(result[1], check[1], dateOnly) and _compareFlags(result[2], check[2])

def _compareTimeTuples(target, value, dateOnly=False):
    """
    Ignores minutes and seconds as running the test could cross a minute
    boundary. Technically the year, month, day, hour, minute, and second could
    all change if the test is run on New Year's Eve, but we won't worry about
    less than per-hour granularity.
    """
    t_yr, t_mth, t_dy, t_hr, t_min, _, _, _, _ = target
    v_yr, v_mth, v_dy, v_hr, v_min, _, _, _, _ = value

    if dateOnly:
        return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy))
    else:
        return ((t_yr == v_yr) and (t_mth == v_mth) and (t_dy == v_dy) and
                (t_hr == v_hr) and (t_min == v_min))

def _compareFlags(result, check):
    return (result == check)
