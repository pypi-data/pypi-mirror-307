import dbm
import enum
import logging
import pathlib
import typing
from types import TracebackType

from pydictcc.entities import DictEntry, Dictionary, Language


class Mode(enum.Enum):
    read = enum.auto()
    write = enum.auto()


class DbmDictionary(Dictionary):
    """An Entry contains a Hash.

    phrase => [translation1, ..., translationN]

    and is heavily used while importing the Dict.cc CSV-file. The String returned
    by to_s() encodes an Entry as string, which becomes the value of some
    keyword in the DBM database. After importing the Dict.cc CSV-file to DBM
    database files the only method used is the static format_str(str), which
    takes a string encoded Entry (DBM-value) and formats them user-friendly.
    """

    def __init__(self, root: pathlib.Path, mode: Mode = Mode.read) -> None:
        self._root = pathlib.Path(root)
        self._mode: Mode = mode
        self._db_path = {
            Language.A: self._root / 'dict_a.pag',
            Language.B: self._root / 'dict_b.pag',
        }
        self._db_instances: dict[Language, dbm] = {
            Language.A: None,
            Language.B: None,
        }
        self._dicts = {
            Language.A: {},
            Language.B: {},
        }

    def __enter__(self) -> Dictionary:
        if self._mode == Mode.read:
            for db_path in self._db_path.values():
                if not db_path.exists():
                    msg = f"There's no {db_path} file! You have to import an dict.cc database file first."
                    raise RuntimeError(msg)

        for lang, path in self._db_path.items():
            self._db_instances[lang] = dbm.open(str(path), 'c' if self._mode == Mode.write else 'r', mode=0o644)
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        for instance in self._db_instances.values():
            instance.close()

    def _expect_mode(self, lang: Language, expect: Mode.read) -> None:
        if expect != self._mode:
            msg = f'Database is used in wrong mode "{self._mode.name}"'
            raise RuntimeError(msg)
        if self._mode == Mode.read and self._db_instances[lang] is None:
            msg = 'Database was used outside of "with" statement'
            raise RuntimeError(msg)

    def clear(self) -> None:
        for d in self._dicts.values():
            d.clear()

    def size(self, lang: Language) -> int:
        if self._mode == Mode.write:
            size = len(self._dicts[lang])
        else:
            self._expect_mode(lang, Mode.read)
            size = sum(1 for _ in self._db_instances[lang].keys())  # noqa: SIM118
        return size

    def add_phrase(self, lang: Language, word: str, phrase: str, translation: str) -> None:
        self._expect_mode(lang, Mode.write)
        if word not in self._dicts[lang]:
            self._dicts[lang][word] = {}
        if phrase not in self._dicts[lang][word]:
            self._dicts[lang][word][phrase] = []

        self._dicts[lang][word][phrase].append(translation)

    @staticmethod
    def _serialize_entry(phrases: dict[str, list[str]]) -> str:
        """Encodes this Entry as string which is used to store entries as values of the DBM database."""
        s = ''
        # Sort by phrase length for shortest to longest match
        sorted_hash = dict(sorted(phrases.items(), key=lambda item: len(item[0])))
        for phrase, translations in sorted_hash.items():
            s += f'{phrase}=<>'
            for translation in translations:
                s += f'{translation}:<>:'
            s = s[:-3] + '#<>#'  # Remove trailing ":<>:" and add separator
        s += '\n'
        return s

    @staticmethod
    def _deserialize_entry(encoded_entry: str) -> dict[str, list[str]]:
        parts = encoded_entry.strip().split('#<>#')
        phrase_trans_dict = {}
        for part in parts:
            if len(part) == 0:
                continue
            phrase, translations_str = part.split('=<>')
            phrase_trans_dict[phrase] = []
            translations = translations_str.split(':<>:')
            for _i, trans in enumerate(translations):
                phrase_trans_dict[phrase].append(trans)
        return phrase_trans_dict

    def write(self) -> None:
        for lang, db_path in self._db_path.items():
            self._expect_mode(lang, Mode.write)

            if db_path.exists():
                logging.debug(f'Going to delete old database {db_path}')
                db_path.unlink()
                logging.info(f'Deleted old database {db_path}')
            if not self._root.exists():
                self._root.mkdir(parents=True, exist_ok=True)

            logging.debug('Writing DBM database file...')
            with dbm.open(str(db_path), 'c', mode=0o644) as fp:
                # Always create a new, empty database, open for reading and writing.
                # with dbm.open(str(self._path), 'c', mode=0o644) as db:
                for idx, (word, phrases) in enumerate(self._dicts[lang].items()):
                    fp[word] = self._serialize_entry(phrases)
                    if idx % 1000 == 0:
                        logging.debug(f'Stored {idx} / {len(self._dicts[lang])} values')
            logging.info(f'Database {lang.name} building for done!')

    def get(self, lang: Language, word: str) -> DictEntry:
        self._expect_mode(lang, Mode.read)

        ret = self._db_instances[lang].get(word.encode(), b'').decode()

        if ret:
            return DictEntry(phrases=self._deserialize_entry(ret))
        return DictEntry(phrases={})

    def iter_words(self, lang: Language) -> typing.Iterator[str]:
        self._expect_mode(lang, Mode.read)

        for key in self._db_instances[lang].keys():  # noqa: SIM118
            yield key.decode()
