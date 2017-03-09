# -*- coding: utf-8 -*-
"""
Preloads fixtures and adds any test hooks or plugins.
"""

import pytest

from tests.lib.assertions import *
from tests.lib.fixtures import *


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.skipped and call.excinfo.errisinstance(pytest.skip.Exception):
        rep.outcome = 'failed'
        r = call.excinfo._getreprcrash()
        message = 'Invalid test configuration'
        if 'empty parameter set' in r.message:
            message = 'No data found for test group'
        rep.longrepr = '%s - %s' % (message, r.message)
