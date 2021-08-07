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
        with open(options.input, 'r') as reader:
            text = reader.read()
    else:
        text = sys.stdin.read()
    text = MONTHS + text
    entries = bibtexparser.loads(text).entries
    problems = {}
    for entry in entries:
        for check in [check_abstract, check_keywords, check_reviewed]:
            check(problems, entry)
    report(problems)


def check_abstract(problems, entry):
    if 'abstract' not in entry:
        record_problem(problems, entry, 'does not have "abstract"')


def check_keywords(problems, entry):
    if 'keywords' not in entry:
        record_problem(problems, entry, 'does not have "keywords"')


def check_reviewed(problems, entry):
    if 'reviewed' not in entry:
        record_problem(problems, entry, 'does not have "reviewed"')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify input file')
    return parser.parse_args()


def record_problem(problems, entry, message):
    assert 'ID' in entry, f'entry {entry} does not have ID'
    if entry['ID'] not in problems:
        problems[entry['ID']] = []
    problems[entry['ID']].append(message)


def report(problems):
    for key in sorted(problems.keys()):
        print(key)
        for message in problems[key]:
            print(f'  {message}')


if __name__ == '__main__':
    main()
