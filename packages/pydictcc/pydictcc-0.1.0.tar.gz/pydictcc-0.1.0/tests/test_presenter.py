import pytest
from pydictcc.entities import DictEntry
from pydictcc.presenter import CompactEntryFormatter, NormalEntryFormatter


@pytest.fixture
def entry() -> DictEntry:
    return DictEntry({'phrase': ['translation 1', 'translation 2']})


def test_normal_presenter(entry: DictEntry) -> None:
    expected_str = """phrase:\n    - translation 1\n    - translation 2\n"""
    assert NormalEntryFormatter()(entry) == expected_str


def test_compact_presenter(entry: DictEntry) -> None:
    expected_str = """- phrase: translation 1 / translation 2\n"""
    assert CompactEntryFormatter()(entry) == expected_str


def test_compact_presenter_wrap(entry: DictEntry) -> None:
    expected_str_15 = """- phrase:\n   translation 1 /\n   translation 2\n"""
    expected_str_30 = """- phrase: translation 1 /\n   translation 2\n"""
    assert CompactEntryFormatter(max_columns=15)(entry) == expected_str_15
    assert CompactEntryFormatter(max_columns=30)(entry) == expected_str_30
