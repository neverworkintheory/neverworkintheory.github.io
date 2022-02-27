import bibtexparser
import re
import sys


LATEX_CHARS = (
    ('---', '—'),
    (r"\`{A}", 'À'),
    (r"\`{E}", 'È'),
    (r"\'{E}", 'É'),
    (r"\'{S}", 'Ś'),
    (r"\'{a}", 'á'),
    (r"\'{c}", 'ć'),
    (r"\`{a}", 'à'),
    (r"\`{e}", 'è'),
    (r"\'{e}", 'é'),
    (r"\'{i}", 'í'),
    (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'),
    (r"\'{\i}", 'í'),
    (r'\"{a}', 'ä'),
    (r'\"{o}', 'ö'),
    (r'\"{u}', 'ü'),
    (r'\'{O}', 'Ó'),
    (r'\'{o}', 'ó'),
    (r'\c{C}', 'Ç'),
    (r'\c{c}', 'ç'),
    (r'\v{S}', 'Š'),
    (r'\v{e}', 'ě'),
    (r'\v{r}', 'ř'),
    (r'\v{s}', 'š'),
    (r'\v{z}', 'ž'),
    (r'\~{a}', 'ã'),
    (r'\~{n}', 'ñ'),
    (r'{\AA}', 'Å'),
    (r'{\aa}', 'å'),
    (r'{\o}', 'ø'),
    (r'\%', '%'),
    (r'\#', '#'),
    (r'${\approx}$', '≈'),
    (r'${\pm}$', '±'),
    (r'${\times}$', '×'),
    (r'\textquotesingle', "'"),
    (r'\textquotedblleft', "'"),
    (r'\textquotedblright', "'"),
    (r'{\ldots}', '…'),
    (r'{\textemdash}', '—'),
    (r'{\textendash}', '–'),
    ('{', ''),
    ('}', ''),
    ('\$', '$'),
    ('\\', ''),
    ('  ', ' '),
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;')
)

LATEX_MACROS = [
    re.compile(r'\\texttt{(.+?)}') # fragile: does not handle nested {}
]


def get_entries(strings=None, source=None):
    strings = open(strings, 'r').read() if (strings is not None) else ''

    if source is None:
        return get_bib('<stdin>', strings, sys.stdin.read())

    if type(source) == str:
        return get_bib(source, strings, open(source, 'r').read())

    entries = [get_bib(filename, strings, open(filename, 'r').read())
               for filename in source]
    entries = [e for sublist in entries for e in sublist]
    return entries


def get_bib(filename, strings, text):
    text = strings + text
    entries = bibtexparser.loads(text).entries
    for e in entries:
        e['FILENAME'] = filename
    return entries


def get_unreviewed(filename):
    '''Get set of unreviewed bibliography entries.'''
    with open(filename, 'r') as reader:
        return set([key.strip() for key in reader])


def unlatex(s):
    '''Remove LaTeX isms.'''
    for pattern in LATEX_MACROS:
        s = pattern.sub(lambda x: x.group(1), s)
    for (original, replacement) in LATEX_CHARS:
        s = s.replace(original, replacement)
    return s
