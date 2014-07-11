# -*- coding: utf-8 -*-
"""
Examples of how to use parsedatetime with locale information provided.

Locale information can come from either PyICU (if available) or from
the more basic internal locale classes that are included in the
`Constants` class.
"""

__license__ = """
Copyright (c) 2004-2006 Mike Taylor
Copyright (c) 2006 Darshana Chhajed
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import parsedatetime as pdt

# create an instance of Constants class so we can specify the locale

c = pdt.Constants("en")
p = pdt.Calendar(c)

# print out the values from Constants to show how the locale information
# is being used/stored internally

values = (c.uses24,                 # 24hr clock?
          c.usesMeridian,           # AM/PM used?
          c.usePyICU,               # was PyICU found/enabled?
          c.meridian,               # list of the am and pm values
          c.am,                     # list of the lowercase and stripped AM string
          c.pm,                     # list of the lowercase and stripped PM string
          c.dateFormats,            # dict of available date format strings
          c.timeFormats,            # dict of available time format strings
          c.timeSep,                # list of time separator, e.g. the ':' in '12:45'
          c.dateSep,                # list of date separator, e.g. the '/' in '11/23/2006'
          c.Months,                 # list of full month names
          c.shortMonths,            # list of the short month names
          c.Weekdays,               # list of the full week day names
          c.localeID                # the locale identifier
          )


print('\n'.join((str(value) for value in values)))


result = p.parse("March 24th")


# create an instance of Constants class and force it not to use PyICU
# and to use the internal Spanish locale class

c = pdt.Constants(localeID="es", usePyICU=False)
p = pdt.Calendar(c)

result = p.parse("Marzo 24")
