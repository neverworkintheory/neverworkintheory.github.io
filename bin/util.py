import bibtexparser
import sys


MONTHS =     '''
@string{jan = "1"}
@string{feb = "2"}
@string{mar = "3"}
@string{apr = "4"}
@string{may = "5"}
@string{jun = "6"}
@string{jul = "7"}
@string{aug = "8"}
@string{sep = "9"}
@string{oct = "10"}
@string{nov = "11"}
@string{dec = "12"}
'''


def get_entries(inputs):
    if not inputs:
        return get_bib('<stdin>', sys.stdin.read())
    entries = [get_bib(f, open(f, 'r').read()) for f in inputs]
    entries = [e for sublist in entries for e in sublist]
    return entries


def get_bib(filename, text):
    text = MONTHS + text
    entries = bibtexparser.loads(text).entries
    for e in entries:
        e['FILENAME'] = filename
    return entries
