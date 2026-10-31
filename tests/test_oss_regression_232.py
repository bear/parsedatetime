"""Regression coverage for date metadata when parsing exact dates."""

import datetime

import pytest

import parsedatetime as pdt


@pytest.mark.parametrize('method', ['parse', 'parseDateText', 'parseDate'])
@pytest.mark.parametrize('source_date, text, numeric, target_date', [
    ((2018, 11, 24), 'December 1st', '12/1', (2018, 12, 1)),
    ((2019, 11, 24), 'January 1st', '1/1', (2020, 1, 1)),
    ((2020, 1, 15), 'February 29th, 2020', '02/29/2020', (2020, 2, 29)),
    ((2019, 1, 15), 'March 1st, 2019', '03/01/2019', (2019, 3, 1)),
])
def test_exact_date_metadata(method, source_date, text, numeric, target_date):
    source = datetime.datetime(*(source_date + (19, 44, 55))).timetuple()
    source = tuple(source[:8]) + (0,)
    expected = datetime.datetime(*(target_date + (19, 44, 55))).timetuple()
    cal = pdt.Calendar(constants=pdt.Constants(localeID='en_US'))
    result = getattr(cal, method)(numeric if method == 'parseDate' else text,
                                  source)
    if method == 'parse':
        result, context = result
        assert context.hasDate
        assert not context.hasTime

    assert result[7] == expected.tm_yday
    assert result[:6] == expected[:6]
    assert result[6] == expected.tm_wday
    assert result[8] == source[8]
