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
