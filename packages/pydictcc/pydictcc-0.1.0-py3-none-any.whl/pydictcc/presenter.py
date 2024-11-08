from pydictcc.entities import DictEntry, DictEntryFormatter


class CompactEntryFormatter(DictEntryFormatter):
    def __init__(self, max_columns: int = 73) -> None:
        self.max_columns = max_columns

    def __call__(self, entry: DictEntry) -> str:
        s = ''
        for phrase, translations in entry.phrases.items():
            s += f'- {phrase}:'
            last_index = len(translations) - 1
            c = len(phrase) + 4
            for i, trans in enumerate(translations):
                if c + 3 + len(trans) >= self.max_columns:
                    c = 3
                    s += '\n   '
                else:
                    s += ' '
                s += trans
                c += 3 + len(trans)
                if i < last_index:
                    s += ' /'
            s += '\n'
        return s


class NormalEntryFormatter(DictEntryFormatter):
    def __call__(self, entry: DictEntry) -> str:
        s = ''
        for phrase, translations in entry.phrases.items():
            s += f'{phrase}:\n'
            s += '\n'.join(f'    - {trans}' for trans in translations)
            s += '\n'
        return s
