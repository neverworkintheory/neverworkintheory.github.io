#!/usr/bin/env python

import argparse
import sys

import util


def main():
    options = get_options()
    entries = util.get_entries(options.strings, options.inputs)
    problems = check(options, entries)
    report(options, problems)


def check(options, entries):
    problems = {}
    for entry in entries:
        for check in [check_abstract]:
            check(options, problems, entry)
    check_overall(options, entries, problems)
    return problems


def check_overall(options, entries, problems):
    seenKeys = set()
    for entry in entries:
        if entry['ID'] in seenKeys:
            record_problem(options, problems, entry, 'has duplicate key')
        seenKeys.add(entry['ID'])


def check_abstract(options, problems, entry):
    if 'abstract' not in entry:
        doi = f'{entry["doi"]} ' if 'doi' in entry else ''
        record_problem(options, problems, entry, f'{doi}does not have "abstract"')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', help='specify bibliography file(s)')
    parser.add_argument('--strings', help='string definitions file (optional)')
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
