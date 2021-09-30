import bibtexparser
import sys


def get_entries(strings, source=None):
    strings = open(strings, 'r').read()

    if source is None:
        return get_bib('<stdin>', strings, sys.stdin.read())

    if type(source) == str:
        return get_bib(source, strings, open(source, 'r').read())

    entries = [get_bib(filename, strings, open(filename, 'r').read())
               for filename in source]
    entries = [e for sublist in entries for e in sublist]
    return entries


def get_bib(filename, strings, text):
    text = strings + text
    entries = bibtexparser.loads(text).entries
    for e in entries:
        e['FILENAME'] = filename
    return entries
