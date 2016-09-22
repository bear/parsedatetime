from .fixtures import pdtFixture


@pdtFixture('numbers_as_words.yml')
def test_numbers_as_words(cal, phrase, target):
    assert cal._convertUnitAsWords(phrase) == target
