# parsedatetime
Parse human-readable date/time strings.

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]

Parsedatetime now targets Python 3 and is currently tested with Python 3.9

Use https://github.com/bear/parsedatetime/releases/tag/v2.6 if you need Python 2.7 compatibility.

## Installing
You can install parsedatetime using
```
pip install parsedatetime
```

## Development environment
Development is done using a `pipenv` virtural environment
```
make env
```

*Note*: `black` is still listed as a beta library, and as such, must be installed with the `--pre` flag

## Running Tests
From the source directory
```
make test
```

To run tests on several Python versions that are installed in the `pipenv` virtual environment
```
$ make tox
[... tox creates a virtualenv for every python version and runs tests inside of each]
py39: commands succeeded
```

The tests depend on PyICU being installed using the `pyicu-binary` package which removes the source build step. PyICU depends on icu4c which on macOS requires homebrew
```
brew install icu4c
```

# Using parsedatetime
Detailed examples can be found in the `examples` directory.

as a time `tuple`
```python
import parsedatetime
    
cal = parsedatetime.Calendar()
cal.parse("tomorrow")
```

as a Python `datetime` object
```python
from datetime import datetime

time_struct, parse_status = cal.parse("tomorrow")
datetime(*time_struct[:6])
```

with timezone support using `pytz`
```python
import parsedatetime
from pytz import timezone

cal = parsedatetime.Calendar()
datetime_obj, _ = cal.parseDT(datetimeString="tomorrow", tzinfo=timezone("US/Pacific"))
```

## Documentation
The generated documentation is included by default in the `docs` directory and can also be viewed online at https://bear.im/code/parsedatetime/docs/index.html

The documentation is generated with
```
make docs
```

## Notes
The `Calendar` class has a member property named `ptc` which is created during the class init method to be an instance of `parsedatetime_consts.CalendarConstants()`.

## History
The code in `parsedatetime` has been implemented over the years in many different languages (C, Clipper, Delphi) as part of different custom/proprietary systems I've worked on.  Sadly the previous code is not "open" in any sense of that word.

When I went to work for Open Source Applications Foundation and realized that the Chandler project could benefit from my experience with parsing of date/time text I decided to start from scratch and implement the code using Python and make it truly open.

After working on the initial concept and creating something that could be shown to the Chandler folks, the code has now evolved to its current state with the help of the Chandler folks, most especially Darshana.

<!-- Badges -->
[pypi-image]: https://img.shields.io/pypi/v/parsedatetime
[pypi-url]: https://pypi.org/project/parsedatetime/
[build-image]: https://circleci.com/gh/bear/parsedatetime.svg?style=svg
[build-url]: https://circleci.com/gh/bear/parsedatetime
[coverage-image]: https://codecov.io/gh/bear/parsedatetime/branch/master/graph/badge.svg
[coverage-url]: https://codecov.io/gh/bear/parsedatetime
