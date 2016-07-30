"""
Unit tests for parsedatetime

The tests can be run as a C{suite} by running::

    nosetests

Requires Python 3.0 or later
"""
import logging


__author__ = 'Mike Taylor (bear@code-bear.com)'
__copyright__ = 'Copyright (c) 2004 Mike Taylor'
__license__ = 'Apache v2.0'
__version__ = '1.0.0'
__contributors__ = ['Darshana Chhajed',
                    'Michael Lim (lim.ck.michael@gmail.com)',
                    'Bernd Zeimetz (bzed@debian.org)',
                    ]


log = logging.getLogger('parsedatetime')
echoHandler = logging.StreamHandler()
echoFormatter = logging.Formatter('%(levelname)-8s %(message)s')
log.addHandler(echoHandler)

# log.setLevel(logging.DEBUG)
