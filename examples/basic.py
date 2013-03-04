"""
Basic examples of how to use parsedatetime
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

# create an instance of Constants class so we can override some of the defaults

c = pdt.Constants()

c.BirthdayEpoch = 80    # BirthdayEpoch controls how parsedatetime
                        # handles two digit years.  If the parsed
                        # value is less than this value then the year
                        # is set to 2000 + the value, otherwise
                        # it's set to 1900 + the value

# create an instance of the Calendar class and pass in our Constants
# object instead of letting it create a default

p = pdt.Calendar(c)

# parse "tomorrow" and return the result

result = p.parse("tomorrow")

# parseDate() is a helper function that bypasses all of the
# natural language stuff and just tries to parse basic dates
# but using the locale information

result = p.parseDate("4/4/80")

# parseDateText() is a helper function that tries to parse
# long-form dates using the locale information

result = p.parseDateText("March 5th, 1980")

