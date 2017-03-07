from datetime import datetime
import pytest

from .data import datedelta


def test_get_years(calendar):
    target = 2
    delta = datedelta(years=target)
    assert delta.years == target


def test_get_months(calendar):
    target = 2
    delta = datedelta(months=target)
    assert delta.months == target


def test_raises_error_on_invalid_types(calendar):
    with pytest.raises(TypeError):
        datedelta(years='bad')
        
    with pytest.raises(TypeError):
        datedelta(months={})
    
    with pytest.raises(TypeError):
        datedelta(sourceTime='bad')


def test_add_years(calendar):
    delta = datedelta(years=2)
    start = datetime(2017, 1, 2)
    target = datetime(2019, 1, 2)
    assert delta.add(start, calendar) == target

    delta = datedelta(years=1)
    start = datetime(2016, 2, 29)
    target = datetime(2017, 2, 28)
    assert delta.add(start, calendar) == target


def test_add_months(calendar):
    delta = datedelta(months=2)
    start = datetime(2017, 1, 2)
    target = datetime(2017, 3, 2)
    assert delta.add(start, calendar) == target

    delta = datedelta(months=1)
    start = datetime(2017, 1, 31)
    target = datetime(2017, 2, 28)
    assert delta.add(start, calendar) == target

    delta = datedelta(months=-1)
    start = datetime(2016, 3, 31)
    target = datetime(2016, 2, 29)
    assert delta.add(start, calendar) == target


def test_add_timedelta(calendar):
    delta = datedelta(days=1, hours=1)
    start = datetime(2017, 1, 2, 9, 0, 0)
    target = datetime(2017, 1, 3, 10, 0, 0)
    assert delta.add(start, calendar) == target


def test_can_only_add_to_datetime(calendar):
    delta = datedelta(years=2)
    with pytest.raises(NotImplementedError):
        delta.add('not a datetime', calendar)


def test_string_representation():
    cases = (
        (datedelta(years=1), '1 year, 0:00:00'),
        (datedelta(years=2, months=6), '2 years, 6 months, 0:00:00'),
        (datedelta(days=1, hours=1, minutes=2, seconds=3), '1 day, 1:02:03'),
        (datedelta(weeks=1, days=1), '8 days, 0:00:00'),
    )
    for (delta, target) in cases:
        assert str(delta) == target


def test_object_representation():
    cases = (
        (datedelta(years=1), 'datedelta(1, 0, datetime.timedelta(0))'),
        (datedelta(years=2, months=6), 'datedelta(2, 6, datetime.timedelta(0))'),
        (datedelta(days=1, hours=1, minutes=2, seconds=3), 'datedelta(0, 0, datetime.timedelta(1, 3723))'),
        (datedelta(weeks=1, days=1), 'datedelta(0, 0, datetime.timedelta(8))'),
    )
    for (delta, target) in cases:
        assert repr(delta) == target
