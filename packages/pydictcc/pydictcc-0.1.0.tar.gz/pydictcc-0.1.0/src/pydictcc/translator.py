import re
import typing

from pydictcc.entities import DictEntry, Dictionary, Language, Translator


class SimpleTranslator(Translator):
    def __call__(self, dictionary: Dictionary, lang: Language, query: str) -> DictEntry:
        """Simple hash lookup. Complexity: O(1)"""
        return dictionary.get(lang, query)


class RegExTranslator(Translator):
    def __call__(self, dictionary: Dictionary, lang: Language, query: str) -> DictEntry:
        """Regexp lookup. Complexity: O(n)"""
        entries = {}
        for key in dictionary.iter_words(lang):
            if re.search(query, key.lower()):
                entries.update(dictionary.get(lang, key).phrases)
        return DictEntry(phrases=entries)


class FulltextTranslator(Translator):
    def __init__(self, progressbar: typing.Callable[[typing.Iterable], typing.Iterable] | None = None) -> None:
        self._progressbar = progressbar

    def __call__(self, dictionary: Dictionary, lang: Language, query: str) -> DictEntry:
        """Fulltext regexp lookup. Complexity: O(n)"""
        entries = {}
        iterator = (
            dictionary.iter_words(lang) if self._progressbar is None else self._progressbar(dictionary.iter_words(lang))
        )
        for key in iterator:
            value: DictEntry = dictionary.get(lang, key)
            for phrase, translations in value.phrases.items():
                match_line_found = False
                if re.search(query, phrase.lower()):
                    match_line_found = True
                    good_translations = translations
                else:
                    good_translations = []
                    for translation in translations:
                        if re.search(query, translation.lower()):
                            match_line_found = True
                            good_translations.append(translation)
                if match_line_found:
                    entries[phrase] = good_translations
        return DictEntry(phrases=entries)
