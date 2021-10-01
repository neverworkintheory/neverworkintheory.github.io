#!/usr/bin/env python

'''Convert BibTeX to YAML.'''

import argparse
import bibtexparser
import re
import string
import sys
import yaml

import util

# ----------------------------------------------------------------------

# Tell YAML to dump full width (no wrapping).
FULL_WIDTH = 100000

# Keys to replace.
REPLACE = {
    'ENTRYTYPE': 'kind',
    'ID': 'key',
    'link': 'url'
}

# Things to remove.
REMOVE = {
    'local',
    'note'
}

def _number_if_possible(s):
    '''Convert to number or return original string.'''
    try:
        return int(s)
    except ValueError:
        return s


PAT_SPLIT = re.compile(r'\s+and\s+')
def _split_names(s):
    '''Split names on 'and'.'''
    return PAT_SPLIT.split(s)


PAT_URL = re.compile(r'\\url{(.+)}')
def _un_url(s):
    '''Remove URL macro.'''
    m = PAT_URL.match(s)
    return m.group(1) if m else s


# Things to convert.
CONVERT = {
    'author': _split_names,
    'editor': _split_names,
    'howpublished': _un_url,
    'number': _number_if_possible,
    'volume': _number_if_possible,
    'year': _number_if_possible
}

LATEX_CHARS = (
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
    (r'\v{z}', 'ž'),
    (r'\~{a}', 'ã'),
    (r'\~{n}', 'ñ'),
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

LATEX_MACROS = [
    re.compile(r'\\texttt{(.+?)}') # fragile: does not handle nested {}
]

# ----------------------------------------------------------------------

def main(args):
    '''Main driver.'''
    options = get_options()
    entries = util.get_entries(options.strings)
    entries = subset(options.only, entries)
    entries = [cleanup(options, entry) for entry in entries]
    result = yaml.dump(entries, width=FULL_WIDTH)
    print(result)


def subset(desired, entries):
    '''Select subset of entries if asked to do so.'''
    if desired:
        desired = set(desired)
        entries = [e for e in entries if e['ID'] in desired]
    return entries


def cleanup(options, entry):
    '''Clean up an entry.'''

    for key in REPLACE:
        if key in entry:
            entry[REPLACE[key]] = entry[key]
            del entry[key]

    for key in REMOVE:
        if key in entry:
            del entry[key]

    for key in CONVERT:
        if key in entry:
            entry[key] = CONVERT[key](entry[key])

    for key in entry:
        if type(entry[key]) == str:
            entry[key] = unlatex(entry[key])
        elif type(entry[key]) == list:
            entry[key] = [unlatex(s) for s in entry[key]]

    return entry


def unlatex(s):
    '''Remove LaTeX isms.'''
    for pattern in LATEX_MACROS:
        s = pattern.sub(lambda x: x.group(1), s)
    for (original, replacement) in LATEX_CHARS:
        s = s.replace(original, replacement)
    return s


def get_options():
    '''Turn arguments into configuration object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='+', help='only convert specified entries (by key)')
    parser.add_argument('--no_abstract', action='store_true', help='skip the abstract')
    parser.add_argument('--strings', help='string definitions file')
    return parser.parse_args()


if __name__ == '__main__':
    main(sys.argv)
