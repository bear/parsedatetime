import os
import pytest
from yaml import YAMLError

from parsedatetime.context import pdtContext
from tests.lib.data import loadData
from tests.lib.models import datedelta, dateReplacement

@pytest.fixture
def basedir():
    return os.path.dirname(__file__)


@pytest.fixture
def constructorData(basedir):
    return loadData(os.path.join(basedir, 'data/en_US/constructors.yml'))


def test_yaml_error(basedir):
    with pytest.raises(YAMLError):
        loadData(os.path.join(basedir, 'data/en_US/yaml_error.yml'))


def test_io_error(basedir):
    with pytest.raises(IOError):
        loadData(os.path.join(basedir, 'data/en_US/does_not_exist.yml'))


def test_datedelta_constructor(constructorData):
    constructorData['datedelta'] == datedelta(years=1, days=1)


def test_dateReplacement_constructor(constructorData):
    constructorData['dateReplacement'] == dateReplacement(month=1, hour=1)
    

def test_pdtContext_constructor(constructorData):
    flags = pdtContext.ACU_YEAR | pdtContext.ACU_HOUR | pdtContext.ACU_SEC
    constructorData['pdtContext'] == pdtContext(flags)
    