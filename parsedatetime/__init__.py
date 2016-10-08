# -*- coding: utf-8 -*-
#
# vim: sw=2 ts=2 sts=2
#
# Copyright 2004-2016 Mike Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
parsedatetime/__init__.py

Parse human-readable date/time text.
Requires Python 2.6 or later
"""

from __future__ import with_statement, absolute_import, unicode_literals

import re
import time
import logging
import warnings
import datetime
import calendar
import contextlib
import email.utils

from .context import Context
from .context_stack import ContextStack
from .constants import Constants, pdtLocales
from .calendar import Calendar, VERSION_FLAG_STYLE, VERSION_CONTEXT_STYLE
from .warns import pdt20DeprecationWarning


__author__ = 'Mike Taylor'
__email__ = 'bear@bear.im'
__copyright__ = 'Copyright (c) 2016 Mike Taylor'
__license__ = 'Apache License 2.0'
__version__ = '2.2'
__url__ = 'https://github.com/bear/parsedatetime'
__download_url__ = 'https://pypi.python.org/pypi/parsedatetime'
__description__ = 'Parse human-readable date/time text.'

# as a library, do *not* setup logging
# see docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
# Set default logging handler to avoid "No handler found" warnings.

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())

__all__ = [
    'Calendar',
    'Constants',
    'Context',
    'ContextStack',
    'pdtLocales',
    'VERSION_FLAG_STYLE',
    'VERSION_CONTEXT_STYLE'
]
