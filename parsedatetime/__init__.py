# -*- coding: utf-8 -*-
#
# vim: sw=2 ts=2 sts=2
#
# Copyright 2004-2021 Mike Taylor
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

"""parsedatetime

Parse human-readable date/time text.

Requires Python 2.7 or later
"""

from __future__ import with_statement, absolute_import, unicode_literals

# ─── Re-export from domain modules ───────────────────────────────────────────

from .pdt_locales import (locales as _locales,
                          get_icu, load_locale,
                          pdtLocales)
from .context import pdtContext, pdtContextStack
from .warns import pdt20DeprecationWarning

# Import Calendar and Constants from the new calendar module
from .calendar import (
    Calendar,
    Constants,
    _initSymbols,
    VERSION_FLAG_STYLE,
    VERSION_CONTEXT_STYLE,
)

# Import time utilities for backward compatibility
from .time_utils import (
    _extract_date,
    _extract_time,
    _pop_time_accuracy,
    _parse_date_w3dtf,
    _parse_date_rfc822,
    _buildTime,
    inc,
)


__author__ = 'Mike Taylor'
__email__ = 'bear@bear.im'
__copyright__ = 'Copyright (c) 2017-2021 Mike Taylor'
__license__ = 'Apache License 2.0'
__version__ = '2.7'
__url__ = 'https://github.com/bear/parsedatetime'
__download_url__ = 'https://pypi.python.org/pypi/parsedatetime'
__description__ = 'Parse human-readable date/time text.'


debug = False
