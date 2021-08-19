#!/usr/bin/env python

import argparse
import bibtexparser
import re
import sys


from util import MONTHS

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
    if options.input:
        with open(options.input, 'r') as reader:
            text = reader.read()
    else:
        text = sys.stdin.read()
    text = MONTHS + text
    entries = bibtexparser.loads(text).entries
    credit = {}
    for entry in entries:
        add_credit(credit, entry)
    report(credit)


def add_credit(credit, entry):
    eid = entry['ID']
    for author in [x.strip() for x in SPLIT.split(entry['author'])]:
        author = unlatex(author)
        author = normalize(author)
        if author not in credit:
            credit[author] = []
        credit[author].append(eid)


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify input file')
    return parser.parse_args()


def report(credit):
    print('<ul>')
    for author in sorted(credit.keys()):
        cites = [f'<a href="/bib/#{c}">{c}</a>' for c in credit[author]]
        print(f'<li>{author}: {", ".join(cites)}</li>')
    print('</ul>')


def normalize(author):
    if author in SPECIAL:
        return SPECIAL[author]
    front, back = author.rsplit(' ', 1)
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
