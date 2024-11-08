import pytest
from pydictcc.builder import build_dictionary, extract_word, parse_line
from pydictcc.entities import DictEntry, Language
from testing.cache_directory import CacheDictionary


# phrase, translation, category, subject
def example_parse_lines() -> list[tuple[str, tuple[str, str, str, str]]]:
    return [
        ('#a	comment', ('', '', '', '')),
        ('', ('', '', '', '')),
        ('abc def', ('', '', '', '')),
        ('abc	def', ('abc', 'def', '', '')),
        ('abc	def	cat', ('abc', 'def', 'cat', '')),
        ('abc	def	cat	[subj.]', ('abc', 'def', 'cat', '[subj.]')),
        ('123	number', ('123', 'number', '', '')),
        ('%a	percent', ('%a', 'percent', '', '')),
        ("'a	apostrophe", ("'a", 'apostrophe', '', '')),
        ('A?	question mark', ('A?', 'question mark', '', '')),
        ('β	beta', ('β', 'beta', '', '')),
        ('”abc.” [info]	”abc.”', ('”abc.” [info]', '”abc.”', '', '')),
        ('[”a”: b]	square brackets', ('[”a”: b]', 'square brackets', '', '')),
        (
            '(a) b [c]	brackets {d} [e: f] [g]	cat	[subj.]',
            ('(a) b [c]', 'brackets {d} [e: f] [g]', 'cat', '[subj.]'),
        ),
    ]


def example_word_extraction() -> list[tuple[str, str]]:
    return [
        ('a bc def ge ', 'def'),
        ('a bc def! ge ', 'def'),
        ('a bc de ge ', 'bc'),
        ('a bc de! ge ', 'bc'),
    ]


def test_cache_builder() -> None:
    dictionary = CacheDictionary()
    dictionary.add_phrase(Language.A, 'word', 'phrase', 'translation')
    item = dictionary.get(Language.A, 'word')
    assert item == DictEntry({'phrase': ['translation']})


@pytest.mark.parametrize(('line', 'translation'), example_parse_lines())
def test_parse_line(line: str, translation: tuple[str, str, str, str]) -> None:
    assert parse_line(line) == translation


@pytest.mark.parametrize(('phrase', 'extracted_word'), example_word_extraction())
def test_extract_word(phrase: str, extracted_word: str) -> None:
    assert extract_word(phrase) == extracted_word


@pytest.mark.parametrize(('line', 'translation'), example_parse_lines())
def test_build_dict(line: str, translation: tuple[str, str, str, str]) -> None:
    dictionary = CacheDictionary()
    build_dictionary(dictionary, line)
    phrase, translation, _, _ = parse_line(line)
    word_a = extract_word(phrase)
    word_b = extract_word(translation)
    if word_a:
        item = dictionary.get(Language.A, word_a)
        assert item == DictEntry({phrase: [translation]})
    else:
        assert dictionary.size(Language.A) == 0

    if word_b:
        item = dictionary.get(Language.B, word_b)
        assert item == DictEntry({translation: [phrase]})
    else:
        assert dictionary.size(Language.B) == 0
