#!/usr/bin/env python

import argparse
import bibtexparser
import re
import sys

import util


SPECIAL = {
    'K. El Emam': 'El Emam, K.',
    'Guilherme Renna Rodrigues': 'Renna Rodrigues, Guilherme',
    'Mel Ó Cinnéide': 'Ó Cinnéide, Mel',
    'Santiago Perez De Rosso': 'Perez De Rosso, Santiago',
    'Arie van Deursen': 'van Deursen, Arie'
}

SPLIT = re.compile(r'\band\b')


def main():
    options = get_options()
    entries = util.get_entries(options.strings, options.input)
    credit = {}
    for entry in entries:
        add_credit(credit, entry)
    report(credit)


def add_credit(credit, entry):
    eid = entry['ID']
    assert ('author' in entry) or ('editor' in entry), \
        f'No author or editor in {entry}'
    source = entry['author'] if ('author' in entry) else entry['editor']
    for person in [x.strip() for x in SPLIT.split(source)]:
        person = unlatex(person)
        person = normalize(person)
        if person not in credit:
            credit[person] = []
        credit[person].append(eid)


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify input file')
    parser.add_argument('--strings', help='string definitions file')
    return parser.parse_args()


def report(credit):
    print('<ul>')
    for person in sorted(credit.keys()):
        cites = [f'<a href="/bib/#{c}">{c}</a>' for c in credit[person]]
        print(f'<li>{person}: {", ".join(cites)}</li>')
    print('</ul>')


def normalize(person):
    if person in SPECIAL:
        return SPECIAL[person]
    front, back = person.rsplit(' ', 1)
    return f'{back}, {front}'

        
def unlatex(s):
    '''Remove LaTeX isms.'''
    return s\
        .replace('---', '—')\
        .replace(r'{\AA}', 'Å')\
        .replace(r'{\aa}', 'å')\
        .replace(r'\"{a}', 'ä')\
        .replace(r"\'{a}", 'á')\
        .replace(r"\'{c}", 'ć')\
        .replace(r"\'{e}", 'é')\
        .replace(r"\'{E}", 'É')\
        .replace(r"{\'{\i}}", 'í')\
        .replace(r"\'{i}", 'í')\
        .replace(r"\'{o}", 'ó')\
        .replace(r"\'{u}", 'ú')\
        .replace(r'\"{o}', 'ö')\
        .replace(r'\'{O}', 'Ó')\
        .replace(r'\'{o}', 'ó')\
        .replace(r'\"{u}', 'ü')\
        .replace(r'{\o}', 'ø')\
        .replace(r'\c{C}', 'Ç')\
        .replace(r'\c{c}', 'ç')\
        .replace(r'\textquotesingle', "'")\
        .replace(r'\textquotedblleft', "'")\
        .replace(r'\textquotedblright', "'")\
        .replace(r'{\ldots}', '…')\
        .replace(r'{\textemdash}', '—')\
        .replace('{', '')\
        .replace('}', '')\
        .replace('\\', '')\
        .replace('  ', ' ')


if __name__ == '__main__':
    main()
