#!/usr/bin/env python

import argparse
import bibtexparser
import sys


MONTHS =     '''
@string{jan = "1"}
@string{feb = "2"}
@string{mar = "3"}
@string{apr = "4"}
@string{may = "5"}
@string{jun = "6"}
@string{jul = "7"}
@string{aug = "8"}
@string{sep = "9"}
@string{oct = "10"}
@string{nov = "11"}
@string{dec = "12"}
'''


def main():
    options = get_options()
    if options.input:
        entries = [get_bib(options, f, open(f, 'r').read()) for f in options.input]
        entries = [e for sublist in entries for e in sublist]
    else:
        entries = get_bib(options, '<stdin>', sys.stdin.read())
    check(options, entries)


def get_bib(options, filename, text):
    text = MONTHS + text
    entries = bibtexparser.loads(text).entries
    for e in entries:
        e['FILENAME'] = filename
    return entries


def check(options, entries):
    problems = {}
    for entry in entries:
        for check in [check_abstract]:
            check(options, problems, entry)
    check_overall(options, entries, problems)
    report(options, problems)


def check_overall(options, entries, problems):
    seenKeys = set()
    for entry in entries:
        if entry['ID'] in seenKeys:
            record_problem(options, problems, entry, 'has duplicate key')
        seenKeys.add(entry['ID'])


def check_abstract(options, problems, entry):
    if 'abstract' not in entry:
        record_problem(options, problems, entry, 'does not have "abstract"')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', nargs='+', help='specify input file(s)')
    return parser.parse_args()


def record_problem(options, problems, entry, message):
    assert 'ID' in entry, f'entry {entry} does not have ID'
    if entry['ID'] not in problems:
        problems[entry['ID']] = []
    problems[entry['ID']].append(message)


def report(options, problems):
    for key in sorted(problems.keys()):
        print(key)
        for message in problems[key]:
            print(f'  {message}')


if __name__ == '__main__':
    main()
