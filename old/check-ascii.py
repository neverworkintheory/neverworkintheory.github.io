#!/usr/bin/env python

'''Check that all characters in .bib files are 7-bit ASCII.'''

import argparse
import sys


def main():
    options = get_options()
    if not options.inputs:
        check('--', sys.stdin)
    else:
        for filename in options.inputs:
            with open(filename, 'r') as reader:
                check(filename, reader)


def check(filename, reader):
    for (i, line) in enumerate(reader):
        problems = [j+1 for (j, char) in enumerate(line) if ord(char) > 127]
        if problems:
            problems = ', '.join([str(j) for j in problems])
            print(f'{filename} {i+1} @ {problems}: {line.rstrip()}')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', help='specify bibliography file(s)')
    return parser.parse_args()


if __name__ == '__main__':
    main()
