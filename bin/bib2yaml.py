#!/usr/bin/env python

'''Convert BibTeX to YAML.'''

import argparse
import bibtexparser
import re
import string
import sys
import yaml

from util import MONTHS


def main(args):
    '''Main driver.'''
    config = parseArgs(args)
    text = BIB_TO_YAML['add'] + sys.stdin.read()
    bib = get_bib(config, text)
    bib = [cleanup(config, entry) for entry in bib]
    result = yaml.dump(bib, width=10000)
    print(result)


def get_bib(config, text):
    '''Read bibliography, filtering if asked to do so.'''
    entries = bibtexparser.loads(text).entries
    if config.only:
        only = set(config.only)
        entries = [e for e in entries if e['ID'] in only]
    return entries


def cleanup(config, entry):
    '''Clean up an entry.'''

    for key in BIB_TO_YAML['replace']:
        if key in entry:
            entry[BIB_TO_YAML['replace'][key]] = entry[key]
            del entry[key]

    for key in BIB_TO_YAML['remove']:
        if key in entry:
            del entry[key]

    for key in BIB_TO_YAML['convert']:
        if key in entry:
            entry[key] = BIB_TO_YAML['convert'][key](entry[key])

    for key in entry:
        if type(entry[key]) == str:
            entry[key] = unlatex(entry[key])
        elif type(entry[key]) == list:
            entry[key] = [unlatex(s) for s in entry[key]]

    return entry


def number_if_possible(s):
    '''Convert to number or return original string.'''
    try:
        return int(s)
    except ValueError:
        return s


def split_names(s):
    '''Split names on 'and'.'''
    return BIB_TO_YAML['split'].split(s)


def un_url(s):
    '''Remove URL macro.'''
    m = BIB_TO_YAML['url'].match(s)
    return m.group(1) if m else s


REPLACEMENTS = (
    ('---', '—'),
    (r"\'{E}", 'É'),
    (r"\'{S}", 'Ś'),
    (r"\'{a}", 'á'),
    (r"\'{c}", 'ć'),
    (r"\'{e}", 'é'),
    (r"\'{i}", 'í'),
    (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'),
    (r"{\'{\i}}", 'í'),
    (r'\"{a}', 'ä'),
    (r'\"{o}', 'ö'),
    (r'\"{u}', 'ü'),
    (r'\'{O}', 'Ó'),
    (r'\'{o}', 'ó'),
    (r'\c{C}', 'Ç'),
    (r'\c{c}', 'ç'),
    (r'\v{r}', 'ř'),
    (r'{\AA}', 'Å'),
    (r'{\aa}', 'å'),
    (r'{\o}', 'ø'),
    (r'\%', '%'),
    (r'\#', '#'),
    (r'${\approx}$', '≈'),
    (r'${\pm}$', '±'),
    (r'${\times}$', '×'),
    (r'\textquotesingle', "'"),
    (r'\textquotedblleft', "'"),
    (r'\textquotedblright', "'"),
    (r'{\ldots}', '…'),
    (r'{\textemdash}', '—'),
    (r'{\textendash}', '–'),
    ('{', ''),
    ('}', ''),
    ('\$', '$'),
    ('\\', ''),
    ('  ', ' '),
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;')
)

PATTERNS = [
    re.compile(r'\\texttt{(.+?)}') # fragile: does not handle nested {}
]


def unlatex(s):
    '''Remove LaTeX isms.'''
    for pattern in PATTERNS:
        s = pattern.sub(lambda x: x.group(1), s)
    for (original, replacement) in REPLACEMENTS:
        s = s.replace(original, replacement)
    return s


# Lookup values for .bib to .yml conversion.
BIB_TO_YAML = {
    # String definitions to add.
    'add': MONTHS,
    # Things to convert.
    'convert': {
        'author': split_names,
        'editor': split_names,
        'howpublished': un_url,
        'number': number_if_possible,
        'volume': number_if_possible,
        'year': number_if_possible
    },
    # Things to remove.
    'remove': {
        'local',
        'note'
    },
    # Keys to replace.
    'replace': {
        'ENTRYTYPE': 'kind',
        'ID': 'key',
        'link': 'url'
    },
    # Splitting author names.
    'split': re.compile(r'\s+and\s+'),
    # Match a URL.
    'url': re.compile(r'\\url{(.+)}')
}


def parseArgs(args):
    '''Turn arguments into configuration object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='+', help='only convert specified entries (by key)')
    parser.add_argument('--no_abstract', action='store_true', help='skip the abstract')
    return parser.parse_args()


if __name__ == '__main__':
    main(sys.argv)
