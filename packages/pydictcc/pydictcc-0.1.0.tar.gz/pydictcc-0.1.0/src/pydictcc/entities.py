import abc
import dataclasses
import enum
import typing


class Language(enum.Enum):
    A = 1
    B = 2


@dataclasses.dataclass(frozen=True)
class DictEntry:
    phrases: dict[str, list[str]]


class Dictionary(abc.ABC):
    @abc.abstractmethod
    def get(self, lang: Language, word: str) -> DictEntry:
        raise NotImplementedError

    @abc.abstractmethod
    def iter_words(self, lang: Language) -> typing.Iterator[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_phrase(self, lang: Language, word: str, phrase: str, translation: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def size(self, lang: Language) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self) -> None:
        raise NotImplementedError


class DictEntryFormatter(abc.ABC):
    @abc.abstractmethod
    def __call__(self, entry: DictEntry) -> str:
        raise NotImplementedError


class Translator(abc.ABC):
    @abc.abstractmethod
    def __call__(self, dictionary: Dictionary, lang: Language, query: str) -> DictEntry:
        raise NotImplementedError
