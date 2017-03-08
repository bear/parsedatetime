import os
import pytest

import tests.lib.fixtures as fixtures
from tests.lib.fixtures import pdtFixture


@pytest.fixture(scope='function', autouse=True)
def patch_generateParameters(mocker):
    mocker.patch.object(fixtures, 'generateParameters')
    
@pytest.fixture
def basedir():
    return os.path.dirname(__file__)


def test_implicit_group_name(basedir):
    filename = 'simple.yml'
    testGroupNames = ['noon']
    parameters = []
    localeIDs = None
    @pdtFixture(filename)
    def test_noon():
        pass
    fixtures.generateParameters.assert_called_once_with(filename, basedir,
                                                        testGroupNames,
                                                        parameters, localeIDs)


def test_explicit_group_name(basedir):
    filename = 'simple.yml'
    testGroupNames = ['noon']
    parameters = []
    localeIDs = None
    @pdtFixture(filename, explicitTestGroupNames=testGroupNames)
    def test_foo():
        pass
    fixtures.generateParameters.assert_called_once_with(filename, basedir,
                                                        testGroupNames,
                                                        parameters, localeIDs)


def test_parameters(basedir):
    filename = 'simple.yml'
    testGroupNames = ['noon']
    parameters = ['a', 'b', 'c']
    localeIDs = None
    @pdtFixture(filename)
    def test_noon(a, b, c):
        pass
    fixtures.generateParameters.assert_called_once_with(filename, basedir,
                                                        testGroupNames,
                                                        parameters, localeIDs)


def test_localeIDs(basedir):
    filename = 'simple.yml'
    testGroupNames = ['noon']
    parameters = []
    localeIDs = ['en_US']
    @pdtFixture(filename, localeIDs=localeIDs)
    def test_noon():
        pass
    fixtures.generateParameters.assert_called_once_with(filename, basedir,
                                                        testGroupNames,
                                                        parameters, localeIDs)


@pdtFixture('simple.yml')
def test_noon(phrase, target):
    """
    explicitTestGroupNames should override the test function name
    """
    assert phrase == 'noon'


@pdtFixture('simple.yml', explicitTestGroupNames=['noon'])
def test_morning(phrase, target):
    """
    explicitTestGroupNames should override the test function name
    """
    assert phrase == 'noon'


@pdtFixture('simple.yml', explicitTestGroupNames=['noon'], localeIDs=['xx'])
@pytest.mark.xfail('Should skip, no tests to run', strict=True)
def test_unknown_locale(phrase, target):
    """
    xfail to ensure that the test is not called for an invalid locale
    """
    pass


@pdtFixture('simple.yml')
@pytest.mark.xfail('Should skip, no tests to run', strict=True)
def test_unknown_group(phrase, target):
    """
    xfail to ensure that the test is not called for a group that does not
    appear in the data file.
    """
    pass
