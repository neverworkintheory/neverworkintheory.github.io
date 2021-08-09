#!/usr/bin/env python

import argparse
import glob
import re

import util

CITE = re.compile(f'<p\s+id="(.+?)"\s+class="bibliography">', re.MULTILINE + re.DOTALL)


def main():
    options = get_options()
    entries = util.get_entries(options.inputs)
    reviewed = get_reviews(options.pagedir)
    problems = check(options, entries, reviewed)
    report(options, problems)


def get_reviews(pagedir):
    reviewed = {}
    for filename in glob.glob(f'{pagedir}/**/*.html', recursive=True):
        with open(filename, 'r') as reader:
            text = reader.read()
            for match in CITE.finditer(text):
                key = match.group(1)
                if key not in reviewed:
                    reviewed[key] = set()
                reviewed[key].add(filename)
    return reviewed


def check(options, entries, reviewed):
    problems = {}
    check_unused(problems, entries, reviewed)
    check_undefined(problems, entries, reviewed)
    return problems


def check_unused(problems, entries, reviewed):
    for entry in entries:
        key = entry['ID']
        if key not in reviewed:
            if key not in problems:
                problems[key] = []
            problems[key].append(f'Key {key} not used')


def check_undefined(problems, entries, reviewed):
    known = {entry['ID'] for entry in entries}
    for key in reviewed:
        if key not in known:
            if key not in problems:
                problems[key] = []
            problems[key].append(f'Key {key} in file {reviewed[key]} not in bibliography')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', help='specify bibliography file(s)')
    parser.add_argument('--pagedir', help='specify root directory of HTML pages')
    return parser.parse_args()


def report(options, problems):
    for key in sorted(problems.keys()):
        for p in problems[key]:
            print(problems[key])


if __name__ == '__main__':
    main()
