import logging
import re
import typing

from pydictcc.entities import Dictionary, Language

NUM_COLUMNS_TRANSLATION = 2
NUM_COLUMNS_TRANSLATION_CATEGORY = 3
NUM_COLUMNS_TRANSLATION_CATEGORY_SUBJECT = 4
NON_WORD_CHARACTERS = re.compile(r'[0-9\t $\-{}\[\]\\.*!¡@#%^&()_+£€¥°„“”–−—=<>₂²³«»ø`´¬¿‹›Ø·§…~|¦√∫ʃ¶⸮⋅ָ∓]')  # noqa: RUF001


def extract_word(phrase: str) -> str:
    """Extract the most important word from the phrase.

    Cause the CSV-file contains phrases we cannot be sure what is the most
    important word. This method strikes out everything between parenthesis, and
    if multiple words stay over, simply takes the longest one.
    """
    w = re.sub(r'\([^)]*\)|\{[^}]*}|\[[^]]*]', '', phrase).strip().lower()
    if not w:
        return ''

    words = re.sub(NON_WORD_CHARACTERS, ' ', w).strip().split()
    if len(words) == 0:
        return ''
    words.sort(key=len, reverse=True)  # Sort by length descending
    word = words[0].strip()
    if len(word) <= 1:
        return ''
    return word


def parse_line(line: str) -> tuple[str, str, str, str]:
    stripped_line = line.strip()

    # Skip empty lines and comments
    if stripped_line.startswith('#') or not stripped_line:
        return '', '', '', ''

    split = stripped_line.split('\t')
    if len(split) == NUM_COLUMNS_TRANSLATION:
        phrase, translation = split
        return phrase.strip(), translation.strip(), '', ''
    if len(split) == NUM_COLUMNS_TRANSLATION_CATEGORY:
        phrase, translation, category = split
        return phrase.strip(), translation.strip(), category.strip(), ''
    if len(split) == NUM_COLUMNS_TRANSLATION_CATEGORY_SUBJECT:
        phrase, translation, category, subject = split
        return phrase.strip(), translation.strip(), category.strip(), subject.strip()

    line_with_visible_tabs = stripped_line.replace('\t', '<t>')
    logging.warning(f"Skipping syntactically broken line '{line_with_visible_tabs}'")

    return '', '', '', ''


def build_dictionary(
    dictionary: Dictionary, content: str, progressbar: typing.Callable[[typing.Iterable], typing.Iterable] | None = None
) -> None:
    """This class builds DBM files from a tab based csv file from http://www.dict.cc."""
    dictionary.clear()
    iterator = content.splitlines() if progressbar is None else progressbar(content.splitlines())
    for line in iterator:
        lang_a, lang_b, _, _ = parse_line(line)
        if not lang_a or not lang_b:
            continue

        word_a = extract_word(lang_a)
        if word_a:
            dictionary.add_phrase(Language.A, word_a, lang_a, lang_b)

        word_b = extract_word(lang_b)
        if word_b:
            dictionary.add_phrase(Language.B, word_b, lang_b, lang_a)
