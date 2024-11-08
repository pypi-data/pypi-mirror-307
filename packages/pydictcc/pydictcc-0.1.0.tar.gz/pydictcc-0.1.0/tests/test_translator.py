import pytest
from pydictcc.entities import DictEntry, Dictionary, Language
from pydictcc.translator import FulltextTranslator, RegExTranslator, SimpleTranslator
from testing.cache_directory import CacheDictionary

queries = ['ab.*', 'abc', 'ghi']
simple_result = [{}, {'abc def': ['ghi']}, {}]
regex_result = [{'abc def': ['ghi']}, {'abc def': ['ghi']}, {}]
fulltext_result = [{'abc def': ['ghi']}, {'abc def': ['ghi']}, {'abc def': ['ghi']}]


@pytest.fixture
def test_dictionary() -> CacheDictionary:
    d = CacheDictionary()
    d.add_phrase(Language.A, 'abc', 'abc def', 'ghi')
    return d


@pytest.mark.parametrize(('query', 'result'), zip(queries, (DictEntry(p) for p in simple_result), strict=True))
def test_simple_translator(test_dictionary: Dictionary, query: str, result: DictEntry) -> None:
    translator = SimpleTranslator()
    assert translator(test_dictionary, Language.A, query) == result


@pytest.mark.parametrize(('query', 'result'), zip(queries, (DictEntry(p) for p in regex_result), strict=True))
def test_regex_translator(test_dictionary: Dictionary, query: str, result: DictEntry) -> None:
    translator = RegExTranslator()
    assert translator(test_dictionary, Language.A, query) == result


@pytest.mark.parametrize(('query', 'result'), zip(queries, (DictEntry(p) for p in fulltext_result), strict=True))
def test_fulltext_translator(test_dictionary: Dictionary, query: str, result: DictEntry) -> None:
    translator = FulltextTranslator()
    assert translator(test_dictionary, Language.A, query) == result
