#!/usr/bin/env python

'''Convert BibTeX to HTML via YAML.'''

import argparse
import bibtexparser
import re
import string
import sys
import yaml

from util import MONTHS


# What do we know how to do?
VERBS = {
    'bib2md',
    'bib2yml',
    'yml2md'
}


def main(args):
    '''Main driver.'''
    config = parseArgs(args)
    check(config.action in VERBS,
          f'Unrecognized verb {config.action}')
    assert config.action in globals(), \
        f'Unknown verb {config.action}'
    result = globals()[config.action](config)
    print(result)

# ----------------------------------------------------------------------

def bib2md(config):
    '''Convert .bib directly to .md.'''
    temp = bib2yml(config)
    return yml2md(config, temp)
    
# ----------------------------------------------------------------------

def bib2yml(config, text=None):
    '''Convert .bib to .yml.'''
    if text is None:
        text = sys.stdin.read()
    text = BIB_TO_YAML['add'] + text
    bib = get_bib(config, text)
    bib = [cleanup(config, entry) for entry in bib]
    return yaml.dump(bib, width=10000)


def get_bib(config, text):
    '''Read bibliography, filtering if asked to do so.'''
    entries = bibtexparser.loads(text).entries
    if config.only:
        only = set(config.only)
        entries = [e for e in entries if e['ID'] in only]
    return entries


# Things to convert.
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


REPLACEMENTS = (
    ('---', '—'),
    (r'{\AA}', 'Å'),
    (r'{\aa}', 'å'),
    (r'\"{a}', 'ä'),
    (r"\'{a}", 'á'),
    (r"\'{c}", 'ć'),
    (r"\'{e}", 'é'),
    (r"\'{E}", 'É'),
    (r"{\'{\i}}", 'í'),
    (r"\'{i}", 'í'),
    (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'),
    (r'\"{o}', 'ö'),
    (r'\'{O}', 'Ó'),
    (r'\'{o}', 'ó'),
    (r'\"{u}', 'ü'),
    (r'{\o}', 'ø'),
    (r'\c{C}', 'Ç'),
    (r'\c{c}', 'ç'),
    (r"\'{S}", 'Ś'),
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

# ----------------------------------------------------------------------

def yml2md(config, text=None):
    '''Convert YAML bibliography to Markdown.'''
    if text is None:
        text = sys.stdin.read()
    data = yaml.load(text, Loader=yaml.FullLoader)
    entries = [] if config.only else [make_toc()]
    letter = chr(ord('A') - 1)
    for entry in data:
        check_entry(entry)
        letter, heading = advance_heading(letter, entry)
        if (not config.only) and (heading is not None):
            entries.append(heading)
        text = YAML_TO_MARKDOWN[entry['kind']](config, entry)
        entries.append(text)
    return '\n\n'.join(entries)


def make_toc():
    '''Make A-Z table of contents for bibliography.'''
    toc = [f'<a href="#{c}">{c}</a>' for c in string.ascii_uppercase]
    return f'<p>{" ".join(toc)}</p>'


def check_entry(entry):
    '''Make sure YAML entry can be turned into Markdown.'''
    check('key' in entry,
          f'Entries must have "key": {entry}')
    check('kind' in entry,
          f'Entries must have "kind": {entry}')
    check(entry['kind'] in YAML_TO_MARKDOWN,
          f'Unknown entry kind {entry["kind"]}')


def advance_heading(letter, entry):
    '''Create the next heading(s)?'''
    first = entry['key'][0]
    if (first == letter):
        return letter, None
    result = []
    letter = chr(ord(letter) + 1)
    while letter <= first:
        result.append(f'<h2 id="{letter}">{letter}</h2>')
        letter = chr(ord(letter) + 1)
    return first, '\n'.join(result)


def article(config, entry):
    '''Convert article to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        article_info(config, entry),
        cite_end(config),
        abstract(config, entry)
    ])


def book(config, entry):
    '''Convert book to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, False),
        book_info(config, entry),
        cite_end(config),
        abstract(config, entry)
    ])


def incollection(config, entry):
    '''Convert chapter in collection to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry, which='author'),
        title(config, entry, True),
        'In ',
        credit(config, entry, which='editor'),
        book_title(config, entry),
        book_info(config, entry),
        cite_end(config),
        abstract(config, entry)
    ])


def inproceedings(config, entry):
    '''Convert proceedings entry to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        proceedings_info(config, entry),
        cite_end(config),
        abstract(config, entry)
    ])


def link(config, entry):
    '''Convert link to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        cite_end(config),
        abstract(config, entry)
    ])


def techreport(config, entry):
    '''Convert techreport to Markdown.'''
    return '\n'.join([
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        cite_end(config),
        abstract(config, entry)
    ])


# Lookup table for entry handlers.
YAML_TO_MARKDOWN = {
    'article': article,
    'book': book,
    'incollection': incollection,
    'inproceedings': inproceedings,
    'link': link,
    'techreport': techreport
}


def abstract(config, entry):
    if config.no_abstract:
        return ''
    check('abstract' in entry,
          f'Entry requires abstract: {str(entry)}')
    return f'<blockquote class="abstract">{entry["abstract"]}</blockquote>'


def article_info(config, entry):
    '''Generate article information.'''
    check(('journal' in entry) and ('year' in entry),
          f'Entry requires journal and year: {str(entry)}')
    details = ''
    if 'volume' in entry:
        details = f'{entry["volume"]}'
    if 'number' in entry:
        details = f'{details}({entry["number"]})'
    if details:
        details = f', {details}'
    doi = f',\n<a class="doi" href="https://doi.org/{entry["doi"]}">{entry["doi"]}</a>' \
        if 'doi' in entry else ''
    return f'<em>{entry["journal"]}</em>{details}, {entry["year"]}{doi}.'


def book_info(config, entry):
    '''Generate book information.'''
    check(('publisher' in entry) and ('year' in entry) and ('isbn' in entry),
          f'Entry requires publisher, year, and ISBN: {entry}')
    return f'{entry["publisher"]}, {entry["year"]}, {entry["isbn"]}.'


def book_title(config, entry):
    '''Generate book title (possibly linking).'''
    check('booktitle' in entry,
          'Entry must have booktitle')
    title = f'<a href="{entry["url"]}">{entry["booktitle"]}</a>' \
        if ('url' in entry) else entry["booktitle"]
    edition = f' ({entry["edition"]} edition)' \
        if ('edition' in entry) else ''
    return f'<em>{title}{edition}.</em>'


def proceedings_info(config, entry):
    '''Generate proceedings entry information.'''
    check('booktitle' in entry,
          f'Entry requires booktitle {entry}')
    doi = f', <a class="doi" href="https://doi.org/{entry["doi"]}">{entry["doi"]}</a>' \
        if 'doi' in entry else ''
    return f'<em>{entry["booktitle"]}</em>{doi}.'


def credit(config, entry, which=None):
    '''Generate credit (author or editor if not specified).'''
    import sys
    names = None
    suffix = ''
    if which is None:
        if 'author' in entry:
            which = 'author'
        elif 'editor' in entry:
            which = 'editor'
    check((which is not None) and (which in entry),
          f'Do not know author or editor for {entry}')
    if which == 'editor':
        suffix = ' (eds.)'
    names = entry[which]
    check(names is not None,
          f'Entry must have author or editor: {entry}')
    if len(names) == 1:
        names = names[0]
    elif len(names) == 2:
        names = f'{names[0]} and {names[1]}'
    elif len(names) > 2:
        front = ', '.join(names[0:-1])
        names = f'{front}, and {names[-1]}'
    return f'{names}{suffix}:'


def title(config, entry, quote):
    '''Generate title (possibly linking and/or quoting).'''
    check('title' in entry,
          f'Entry {entry} does not have title')
    title = f'<a href="{entry["url"]}">{entry["title"]}</a>' \
        if ('url' in entry) else entry["title"]
    title = f'"{title}"' if quote else f'<em>{title}</em>'
    edition = f' ({entry["edition"]} edition)' \
        if ('edition' in entry) else ''
    return f'{title}{edition}.'


def cite_start(config, entry):
    '''Generate bibliography key in start of entry.'''
    check('key' in entry,
          'Every entry must have key')
    key = entry["key"]
    return f'<p id="{key}" class="bib"><cite>{key}</cite>'


def cite_end(config):
    '''Finish an entry.'''
    return '</p>'

# -------------------------------------------------------------------------------

def check(cond, msg):
    '''Conditional failure.'''
    if not cond:
        fail(msg)


def fail(msg):
    '''Unilateral failure.'''
    print(msg, file=sys.stderr)
    sys.exit(1)


def parseArgs(args):
    '''Turn arguments into configuration object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help=f'allowed actions {", ".join(sorted(VERBS))}')
    parser.add_argument('--only', nargs='+', help='only convert specified entries (by key)')
    parser.add_argument('--link', action='store_true', help='use a link instead of a span for the citation key')
    parser.add_argument('--no_abstract', action='store_true', help='skip the abstract')
    return parser.parse_args()

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
