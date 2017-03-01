from datetime import datetime
import pytest

from .data import dateReplacement


def test_replace():
    replacement = dateReplacement(
        year=1,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )
    source = datetime.now()
    target = datetime(1, 1, 1, 1, 1, 1, source.microsecond)
    assert replacement.replace(source) == target


def test_wildcard_string():
    wildcard = '1111-12-13 14:15:16'
    target = dateReplacement(
        year=1111,
        month=12,
        day=13,
        hour=14,
        minute=15,
        second=16,
    )
    assert dateReplacement.fromWildcardString(wildcard) == target


def test_wildcard_string_supports_omission_of_leading_zero():
    wildcard = '1-2-3 4:5:6'
    target = dateReplacement(
        year=1,
        month=2,
        day=3,
        hour=4,
        minute=5,
        second=6,
    )
    assert dateReplacement.fromWildcardString(wildcard) == target


def test_wildcard_string_ignores_partial_replacements():
    wildcard = '12xx-1x-1x 1x:1x:1x'
    target = dateReplacement()
    assert dateReplacement.fromWildcardString(wildcard) == target


def test_raises_error_on_invalid_wildcard_strings():
    wildcard = '1111-12-13 14:15:16:xx'
    with pytest.raises(ValueError):
        dateReplacement.fromWildcardString(wildcard)

    wildcard = '1111-12-13'
    with pytest.raises(ValueError):
        dateReplacement.fromWildcardString(wildcard)


def test_raises_error_on_invalid_kwargs():
    with pytest.raises(TypeError):
        dateReplacement(foo=1)


def test_accepts_all_datetime_replace_kwargs():
    dateReplacement(
        year=1,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        microsecond=1,
        tzinfo=None,
    )
