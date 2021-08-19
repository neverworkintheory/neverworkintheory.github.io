#!/usr/bin/env python

'''Select a paper at random.'''

import bibtexparser
import random
import sys

from util import MONTHS


def main():
    text = MONTHS + sys.stdin.read()
    entries = bibtexparser.loads(text).entries
    entry = random.choice(entries)
    print(entry['ID'], entry['title'])


if __name__ == '__main__':
    main()
