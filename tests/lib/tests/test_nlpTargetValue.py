from datetime import datetime
import pytest

from tests.lib.data import nlpTargetValue
from parsedatetime.context import pdtContext


def test_values():
    phrase = 'now'
    target = datetime.now()
    context = pdtContext(pdtContext.ACU_NOW)
    startIndex = 12
    target_value = nlpTargetValue(phrase, target, context=context,
                                  startIndex=startIndex)
    assert target_value.phrase == phrase
    assert target_value.target == target
    assert target_value.context == context
    assert target_value.startIndex == startIndex


def test_defaults_to_wildcard_context():
    target_value = nlpTargetValue('now', datetime.now())
    assert target_value.context == pdtContext(pdtContext.ACU_WILDCARD)


def test_wrong_phrase_type():
    with pytest.raises(TypeError):
        nlpTargetValue(1, datetime.now())


def test_wrong_context_type():
    with pytest.raises(TypeError):
        nlpTargetValue('now', datetime.now(), context=1)


def test_wrong_startIndex_type():
    with pytest.raises(TypeError):
        nlpTargetValue('now', datetime.now(), startIndex='bad')

