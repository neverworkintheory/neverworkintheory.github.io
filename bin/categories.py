#!/usr/bin/env python

import re
import sys


CATEGORIES = re.compile(r'^categories:\s*\[(.+?)\]', re.MULTILINE)


def main():
    categories = {}
    for filename in sys.argv[1:]:
        get_categories(categories, filename)
    report(categories)


def get_categories(categories, filename):
    with open(filename, 'r') as reader:
        text = reader.read()
        match = CATEGORIES.search(text)
        if not match:
            print(f'No categories in {filename}', file=sys.stderr)
            return
        for cat in [x.strip().strip('"') for x in match.group(1).split(',')]:
            if cat not in categories:
                categories[cat] = set()
            categories[cat].add(filename)


def report(categories):
    for cat in sorted(categories.keys()):
        print(f'{cat}: {len(categories[cat])}')
        for filename in sorted(categories[cat]):
            print(f'  {filename}')


if __name__ == '__main__':
    main()
