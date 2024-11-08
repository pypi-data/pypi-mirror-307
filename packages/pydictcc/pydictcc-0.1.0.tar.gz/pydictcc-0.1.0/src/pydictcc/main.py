#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
import sys

try:
    import tqdm
except ImportError:
    tqdm = None

from pydictcc.builder import build_dictionary
from pydictcc.dbm_dictionary import DbmDictionary, Mode
from pydictcc.entities import Dictionary, Language
from pydictcc.presenter import CompactEntryFormatter, NormalEntryFormatter
from pydictcc.translator import FulltextTranslator, RegExTranslator, SimpleTranslator


def get_share_dir(app_name: str) -> pathlib.Path:
    share_dir = os.getenv('XDG_DATA_HOME', pathlib.Path(os.environ['HOME']) / '.local' / 'share')
    return pathlib.Path(share_dir) / app_name


def build(dictionary: Dictionary, args: argparse.Namespace) -> None:
    logging.info(f'Reading dict file ({args.import_file})')
    with args.import_file.open() as fp:
        content = fp.read()

    progressbar = None if tqdm is None else tqdm.tqdm
    build_dictionary(dictionary, content, progressbar=progressbar)
    dictionary.write()


def translate(dictionary: Dictionary, args: argparse.Namespace) -> None:
    query = ' '.join(args.query)
    if query.startswith(':r/') or args.regex:
        translate_fct = RegExTranslator()
        if query.startswith(':r/'):
            query = query[3:]
    elif query.startswith(':f/') or args.fulltext:
        progressbar = None if tqdm is None else tqdm.tqdm
        translate_fct = FulltextTranslator(progressbar=progressbar)
        if query.startswith(':f/'):
            query = query[3:]
    else:
        translate_fct = SimpleTranslator()
    formatter = CompactEntryFormatter() if args.compact else NormalEntryFormatter()

    for lang in [Language.A, Language.B]:
        other = Language.B if lang == Language.A else lang.A
        print(f'====================[ {lang.name} -> {other.name} ]====================')
        print(formatter(translate_fct(dictionary, lang, query)))


def make_arg_parser() -> argparse.ArgumentParser:
    default_dict_dir = get_share_dir('pydictcc')
    parser = argparse.ArgumentParser(prog='pydictcc', add_help=False)
    build_group = parser.add_argument_group('Dictionary building options')
    build_group.add_argument(
        '-i', '--import', metavar='DICTCC_FILE', help='Import the dict.cc file', dest='import_file', type=pathlib.Path
    )
    build_group.add_argument(
        '-d', '--directory', metavar='PATH', help='Storage directory', default=default_dict_dir, type=pathlib.Path
    )
    misc_group = parser.add_argument_group('Misc options')
    misc_group.add_argument('-h', '--help', action='help', help='show this help message and exit')
    misc_group.add_argument('-v', '--version', help='Show version', action='version', version='<2014-10-14>')
    misc_group.add_argument('-S', '--size', action='store_true', help='Show the number of entries in the databases')
    format_group = parser.add_argument_group('Format options')
    format_group.add_argument('-c', '--compact', action='store_true', help='Use compact output format')
    query_group = parser.add_argument_group('Query option')
    query_group.add_argument('-s', '--simple', action='store_true', help='Translate the word given as QUERY (default)')
    query_group.add_argument('-r', '--regex', action='store_true', help='Translate all words matching the regexp QUERY')
    query_group.add_argument('-f', '--fulltext', action='store_true', help='Translate all phrases matching the QUERY')
    parser.add_argument('query', nargs='*', metavar='QUERY', help='query')
    return parser


def main() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = make_arg_parser()
    args = parser.parse_args()

    try:
        if args.import_file is not None:
            with DbmDictionary(args.directory, mode=Mode.write) as dictionary:
                build(dictionary, args)
        elif args.size:
            with DbmDictionary(args.directory) as dictionary:
                print(f'Dictionary {Language.A} -> {Language.B} has {dictionary.size(Language.A)} entries')
                print(f'Dictionary {Language.B} -> {Language.A } has {dictionary.size(Language.B)} entries')
        else:
            with DbmDictionary(args.directory) as dictionary:
                translate(dictionary, args)

    except RuntimeError as e:
        print(f'Error:\n{e}\n\n', file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
