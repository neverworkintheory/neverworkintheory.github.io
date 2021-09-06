#!/usr/bin/env python

'''Show all papers (for a specified year).'''

import bibtexparser
import random
import sys

from util import MONTHS


def main():
    text = MONTHS + sys.stdin.read()
    entries = bibtexparser.loads(text).entries
    if len(sys.argv) == 2:
        year = sys.argv[1]
        entries = [e for e in entries if year in e['ID']]
    if not entries:
        print('No entries available', file=sys.stderr)
    else:
        for entry in entries:
            print(f"{entry['ID']}: {entry['title']}")


if __name__ == '__main__':
    main()
