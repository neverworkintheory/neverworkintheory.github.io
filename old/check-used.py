#!/usr/bin/env python

import argparse
import glob
import re

import util


CITE = re.compile('<cite>(.+?)</cite>', re.MULTILINE + re.DOTALL)


def main():
    options = get_options()
    used = util.get_entries(options.strings, options.used)
    unreviewed = util.get_unreviewed(options.unreviewed)
    mentions = get_mentions(options.pagedir)
    problems = check(options, used, mentions, unreviewed)
    report(options, problems)


def get_mentions(pagedir):
    mentions = {}
    for filename in glob.glob(f'{pagedir}/**/*.html', recursive=True):
        with open(filename, 'r') as reader:
            text = reader.read()
            for cite in CITE.finditer(text):
                for key in [k.strip() for k in cite.group(1).split(',')]:
                    if key not in mentions:
                        mentions[key] = set()
                    mentions[key].add(filename)
    return mentions


def check(options, used, mentions, unreviewed):
    problems = []
    check_missing(options, used, mentions, problems)
    check_unmentioned(options, used, mentions, problems)
    check_unreviewed(options, used, unreviewed, problems)
    return problems


def check_missing(options, used, mentions, problems):
    missing = mentions.keys() - {entry['ID'] for entry in used}
    problems.extend([f'{key} in {", ".join(mentions[key])} not in bibliography' for key in missing])


def check_unmentioned(options, used, mentions, problems):
    unmentioned = {entry['ID'] for entry in used} - mentions.keys()
    problems.extend([f'{key} not mentioned' for key in unmentioned])


def check_unreviewed(options, used, unreviewed, problems):
    for entry in used:
        if entry['ID'] in unreviewed:
            continue
        if 'reviewed' in entry:
            continue
        problems.append(f'{entry["ID"]} does not have review date')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pagedir', help='specify root directory of HTML pages')
    parser.add_argument('--strings', help='string definitions file')
    parser.add_argument('--used', help='.bib file with used entries')
    parser.add_argument('--unreviewed', help='text file with one key per line indicating unreviewed entries')
    return parser.parse_args()


def report(options, problems):
    for p in sorted(problems):
        print(p)


if __name__ == '__main__':
    main()
