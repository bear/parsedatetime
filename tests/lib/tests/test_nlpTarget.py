from datetime import datetime
import pytest

from tests.lib.models import nlpTarget, TestCase


@pytest.fixture
def nowTargets():
    return [{
        'phrase': 'now',
        'target': datetime.now(),
    }]

@pytest.fixture
def testCase(calendar):
    caseData = {
        'phrases': ['now'],
        'target': datetime.now(),
    }
    return TestCase(caseData, calendar, datetime.now())

otherTestCase = testCase


def test_equality(nowTargets, testCase, otherTestCase):
    sourcePhrase = 'test now'
    target = nlpTarget(nowTargets, testCase, sourcePhrase)
    otherTarget = nlpTarget(nowTargets, otherTestCase, sourcePhrase)
    assert target == otherTarget
    assert target == otherTarget.tupleValue
    assert not (target == 5)


def test_explicit_startIndex(nowTargets, testCase, otherTestCase):
    sourcePhrase = 'test now'
    startIndex = 11
    nowTargets[0]['startIndex'] = startIndex
    target = nlpTarget(nowTargets, testCase, sourcePhrase)
    assert target.tupleValue[0][2] == startIndex
    assert target.tupleValue[0][3] == startIndex + len('now')


def test_object_representation(nowTargets, testCase):
    sourcePhrase = 'test now'
    now = nowTargets[0]['target']
    target = nlpTarget(nowTargets, testCase, sourcePhrase)
    representation = 'nlpTarget((%r, pdtContext(), 5, 8, \'now\'),)' % now
    assert repr(target) == representation


def test_raises_error_for_phrase_not_in_sourcePhrase(nowTargets, testCase):
    sourcePhrase = 'test'
    target = nlpTarget(nowTargets, testCase, sourcePhrase)
    with pytest.raises(ValueError) as excinfo:
        target.tupleValue
    assert excinfo.match(r'\bphrase\b.*\bnot contained\b')


def test_raises_error_for_no_testCase(nowTargets):
    sourcePhrase = 'test'
    target = nlpTarget(nowTargets, sourcePhrase=sourcePhrase)
    with pytest.raises(ValueError) as excinfo:
        target.tupleValue
    assert excinfo.match(r'\btestCase\b')


def test_raises_error_for_no_sourcePhrase(nowTargets, testCase):
    sourcePhrase = 'test'
    target = nlpTarget(nowTargets, testCase)
    with pytest.raises(ValueError) as excinfo:
        target.tupleValue
    assert excinfo.match(r'\bsourcePhrase\b')
