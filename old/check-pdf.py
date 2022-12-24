#!/usr/bin/env python

'''Check bibliography files against .bib files.'''

import argparse
import bibtexparser
import glob
import re
import sys

import util


PDF_PAT = re.compile(r'.*/([^/]+).pdf')

SKIP_ENTRIES = {
    'book',
    'incollection'
}


def main():
    options = get_options()

    entries = util.get_entries(options.strings, options.inputs)
    entries = [e for e in entries
               if ((e['ENTRYTYPE'] not in SKIP_ENTRIES) and ('doi' in e))]
    bibKeys = {e['ID'] for e in entries}

    pdf = get_pdfs(options.pdfdir)
    pdfKeys = {k.split('-')[0] for k in pdf.keys()}

    report('BibTeX but no PDF', bibKeys - pdfKeys, entries)
    report('PDF but no BibTeX', pdfKeys - bibKeys, entries)


def get_pdfs(pdfdir):
    pattern = f'{pdfdir}/**/*.pdf'
    result = {}
    for filename in glob.iglob(pattern, recursive=True):
        match = PDF_PAT.search(filename)
        assert match, f'{filename} does not match regexp'
        key = match.group(1)
        result[key] = filename
    return result


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', help='bibliography file(s)')
    parser.add_argument('--pdfdir', help='root directory of PDF files')
    parser.add_argument('--strings', help='string definitions file')
    return parser.parse_args()


def report(msg, keys, bib):
    if not keys:
        return
    print(msg)
    for k in sorted(keys):
        if k not in bib:
            print(f'- {k}')
        else:
            entry = bib[k]
            doi = entry['doi'] if 'doi' in entry else 'missing DOI'
            print(f'- {k}: {doi}')


if __name__ == '__main__':
    main()
