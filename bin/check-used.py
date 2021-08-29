#!/usr/bin/env python

import argparse
import glob
import re

import util

CITE = re.compile('<a.+?class="bibkey".+?>', re.MULTILINE + re.DOTALL)
HREF = re.compile('href="/bib/#(.+?)"')


def main():
    options = get_options()
    used = util.get_entries(options.used)
    mentions = get_mentions(options.pagedir)
    problems = check(options, used, mentions)
    report(options, problems)


def get_mentions(pagedir):
    mentions = {}
    for filename in glob.glob(f'{pagedir}/**/*.html', recursive=True):
        with open(filename, 'r') as reader:
            text = reader.read()
            for cite in CITE.finditer(text):
                href = HREF.search(cite.group(0))
                assert href, f'Badly-formatted citation {cite}'
                key = href.group(1)
                if key not in mentions:
                    mentions[key] = set()
                mentions[key].add(filename)
    return mentions


def check(options, used, mentions):
    problems = []
    check_missing(options, used, mentions, problems)
    check_unmentioned(options, used, mentions, problems)
    return problems


def check_missing(options, used, mentions, problems):
    missing = mentions.keys() - {entry['ID'] for entry in used}
    problems.extend([f'{key} in {", ".join(mentions[key])} not in bibliography' for key in missing])


def check_unmentioned(options, used, mentions, problems):
    unmentioned = {entry['ID'] for entry in used} - mentions.keys()
    problems.extend([f'{key} not mentioned' for key in unmentioned])


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pagedir', help='specify root directory of HTML pages')
    parser.add_argument('--used', help='.bib file with used entries')
    parser.add_argument('--todo', help='.bib file with todo entries')
    return parser.parse_args()


def report(options, problems):
    for p in sorted(problems):
        print(p)


if __name__ == '__main__':
    main()
