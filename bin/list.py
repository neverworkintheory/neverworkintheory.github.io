#!/usr/bin/env python

'''Select a paper at random.'''

import argparse
import bibtexparser
import random
import re
import sys

import util


SORT_KEY = re.compile(r'^(.+)(\d{4})(.*?)$')


def main():
    options = get_options()
    entries = util.get_entries(*options.input)
    if options.year:
        entries = [e for e in entries if options.year in e['ID']]
    if options.random:
        entries = [random.choice(entries)]
    entries.sort(key=sortKey)
    for e in entries:
        print(e['ID'], e['title'])


def sortKey(entry):
    '''Create a sorting key for an entry.'''
    match = SORT_KEY.match(entry['ID'])
    suffix = f'+{match.group(3)}' if match.group(3) else ''
    return (match.group(2), match.group(1) + suffix)


def get_options():
    '''Turn arguments into configuration object.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', nargs='+', help='specify input file(s)')
    parser.add_argument('--random', action='store_true', help='select a single random entry')
    parser.add_argument('--year', nargs='?', help='specify a year')
    return parser.parse_args()


if __name__ == '__main__':
    main()
