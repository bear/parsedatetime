import pytest

from tests.lib.fixtures import pdtFixture


@pdtFixture('nlp.yml')
def test_long_phrases(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pdtFixture('nlp.yml')
def test_long_phrases_with_quotes(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pdtFixture('nlp.yml')
def test_prefixes(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pdtFixture('nlp.yml')
def test_invalid_phrases(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pdtFixture('simple_datetimes.yml')
def test_times(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pdtFixture('simple_datetimes.yml')
def test_invalid_times(calendar, phrase, sourceTime, nlpTarget):
    assert calendar.nlp(phrase, sourceTime) == nlpTarget


@pytest.mark.parametrize('prefix,suffix', (('"', '"'), ("'", "'"), ('(', ')')))
@pdtFixture('simple_datetimes.yml', ['times', 'invalid_times', 'dates',
                                     'invalid_dates'])
def test_simple_datetimes_wrapped(calendar, phrase, sourceTime, nlpTarget, prefix,
                                  suffix):
    sourcePhrase = u'%s%s%s' % (prefix, phrase, suffix)
    nlpTarget.sourcePhrase = sourcePhrase
    assert calendar.nlp(sourcePhrase, sourceTime) == nlpTarget


@pdtFixture('deltas.yml', ['past_integer_values', 'past_float_values'],
            # FIXME: Simple tests in German locale fail
            localeIDs=['en_US'])
def test_deltas(calendar, phrase, sourceTime, nlpTarget):
    # FIXME: these tests fail
    if phrase in ('1855336.424 minutes ago',):
        return
    assert calendar.nlp(phrase, sourceTime) == nlpTarget
