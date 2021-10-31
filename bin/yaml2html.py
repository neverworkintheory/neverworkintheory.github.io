#!/usr/bin/env python

'''Convert YAML bibliography to HTML.'''

import argparse
import re
import string
import sys
import yaml


def main(args):
    '''Main driver.'''
    config = parseArgs(args)
    template = read_template(config)
    text = sys.stdin.read()
    data = yaml.load(text, Loader=yaml.FullLoader)
    entries = [] if config.notoc else [make_toc()]
    letter = chr(ord('A') - 1)
    for entry in data:
        check_entry(entry)
        letter, heading = advance_heading(letter, entry)
        if (not config.notoc) and (heading is not None):
            entries.append(heading)
        fields = YAML_TO_MARKDOWN[entry['kind']](config, entry)
        text = '\n'.join([x for x in fields if x])
        entries.append(text)
    result = '\n\n'.join(entries)
    print(template)
    print(result)


def read_template(config):
    '''Read template if any specified, or return empty string.'''
    if config.template is None:
        return ''
    with open(config.template, 'r') as reader:
        return reader.read().rstrip()


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
    return [
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        article_info(config, entry),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


def book(config, entry):
    '''Convert book to Markdown.'''
    return [
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, False),
        book_info(config, entry),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


def incollection(config, entry):
    '''Convert chapter in collection to Markdown.'''
    return [
        cite_start(config, entry),
        credit(config, entry, which='author'),
        title(config, entry, True),
        'In ',
        credit(config, entry, which='editor'),
        book_title(config, entry),
        book_info(config, entry),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


def inproceedings(config, entry):
    '''Convert proceedings entry to Markdown.'''
    return [
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        proceedings_info(config, entry),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


def link(config, entry):
    '''Convert link to Markdown.'''
    return [
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


def misc(config, entry):
    '''Convert misc to Markdown.'''
    return link(config, entry)


def techreport(config, entry):
    '''Convert techreport to Markdown.'''
    return [
        cite_start(config, entry),
        credit(config, entry),
        title(config, entry, True),
        reviewed(config, entry),
        cite_end(config),
        abstract(config, entry)
    ]


# Lookup table for entry handlers.
YAML_TO_MARKDOWN = {
    'article': article,
    'book': book,
    'incollection': incollection,
    'inproceedings': inproceedings,
    'link': link,
    'misc': misc,
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
    check(('publisher' in entry) and ('year' in entry),
          f'Entry requires publisher and year: {entry}')
    check(('isbn' in entry) or ('howpublished' in entry),
          f'Entry requires ISBN or howpublished: {entry}')
    details = entry["isbn"] if 'isbn' in entry \
        else f'<a href="{entry["howpublished"]}">{entry["howpublished"]}</a>'
    return f'{entry["publisher"]}, {entry["year"]}, {details}.'


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
    check(('booktitle' in entry) and ('year' in entry),
          f'Entry requires booktitle and year {entry}')
    year = entry['year']
    doi = f', <a class="doi" href="https://doi.org/{entry["doi"]}">{entry["doi"]}</a>' \
        if 'doi' in entry else ''
    return f'<em>{entry["booktitle"]}</em>, {year}{doi}.'


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
    elif len(names) > 8:
        names = f'{names[0]} and {len(names) - 1} others'
    else:
        front = ', '.join(names[0:-1])
        names = f'{front}, and {names[-1]}'
    return f'{names}{suffix}:'


def reviewed(config, entry):
    '''Include link to review (if any).'''
    if 'reviewed' not in entry:
        return ''
    url = entry['reviewed'] # /YYYY/MM/DD/title.html
    date = '-'.join(url.split('/')[1:4]) # YYYY-MM-DD
    return f' (Reviewed <a href="{{{{\'{url}\' | relative_url}}}}">{date}</a>.)'


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
    parser.add_argument('--notoc', action='store_true', help='do not create a table of contents')
    parser.add_argument('--no_abstract', action='store_true', help='skip the abstract')
    parser.add_argument('--template', help='specify template file (default none)')
    return parser.parse_args()

if __name__ == '__main__':
    main(sys.argv)
