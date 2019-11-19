import os
import pytest

from tests.lib.fixtures import generateParameters


@pytest.fixture
def basedir():
    return os.path.dirname(__file__)


def test_empty_file(basedir):
    parameters = ['target', 'phrase']
    result = generateParameters('empty.yml', basedir, [], parameters)
    assert result == (','.join(parameters), [])


def test_known_parameters(basedir):
    targetParameters = [
        'sourceTime',
        'target',
        'phrase',
        'context',
        'calendar',
        'nlpTarget',
        'case',
    ]
    parameters = targetParameters + ['unknown']
    result = generateParameters('empty.yml', basedir, [], parameters)
    assert result == (','.join(targetParameters), [])


def test_unknown_locales(basedir):
    parameters = ['target']
    result = generateParameters('simple.yml', basedir, [], parameters,
                                localeIDs=['xx', 'yy'])
    assert result == (','.join(parameters), [])
