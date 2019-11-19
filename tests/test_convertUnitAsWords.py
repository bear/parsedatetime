from tests.lib.fixtures import pdtFixture


@pdtFixture('numbers_as_words.yml')
def test_numbers_as_words(calendar, phrase, target):
    assert calendar._convertUnitAsWords(phrase) == target
