"""Extract information from bibliography."""

import argparse
import sys
import yaml

from pybtex.database import parse_string


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

SIMPLIFY_CHARS = (
    ('Å', 'A'),
    ('Ś', 'S'),
)


def main():
    """Main driver."""
    config = _parse_args()
    bib = _read_bib(config.bib, config.strings)
    unreviewed = _read_unreviewed(config.unreviewed)
    bib = _remove_unreviewed(bib, unreviewed)

    authors = _by_author(bib)

    writer = open(config.output, "w") if config.output else sys.stdout
    yaml.dump(authors, writer)


def _clean(text):
    """Clean up LaTeX characters in a string."""
    text = str(text)
    for (latex, html) in LATEX_CHARS:
        text = text.replace(latex, html)
    return text


def _by_author(bib):
    """Convert entries to YAML of 'author' => [{'date', 'key', 'reviewed'}]."""
    accum = {}

    for key in bib.keys():
        if "reviewed" not in bib[key].fields:
            print(f"Unreviewed {key}", file=sys.stderr)
            continue
        reviewed = bib[key].fields["reviewed"]
        for p in bib[key].persons:
            for name in bib[key].persons[p]:
                date = _post_to_date(reviewed)
                accum.setdefault(_clean(name), set()).add((date, key, reviewed))

    result = []
    for name in sorted(accum.keys(), key=_simplify_name):
        entries = list(sorted(accum[name]))
        entries = [{"date": i[0], "key": i[1], "reviewed": i[2]} for i in entries]
        result.append({"name": name, "entries": entries})
        
    return result


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--bib", help="Bibliography BibTeX file")
    parser.add_argument("--output", help="Output file", default=None)
    parser.add_argument("--strings", help="String definitions BibTeX file")
    parser.add_argument("--unreviewed", help="Plaintext file with keys of unreviewed items")
    return parser.parse_args()


def _post_to_date(filename):
    """Convert post filename to date."""
    return "-".join(filename.split("/")[1:4])


def _read_unreviewed(unreviewed):
    """Read keys of unreviewed bibliography entries."""
    lines = open(unreviewed, "r").readlines()
    lines = [ln.strip() for ln in lines]
    return {ln for ln in lines if ln}


def _remove_unreviewed(bib, unreviewed):
    """Remove unreviewed items from bibliography."""
    return {k:bib[k] for k in bib.keys() if k not in unreviewed}


def _read_bib(bib_path, strings_path):
    """Read bibliography and strings and convert."""
    bib = open(bib_path, "r").read()
    strings = open(strings_path, "r").read()
    bib = strings + "\n\n" + bib
    return parse_string(bib, "bibtex").entries


def _simplify_name(name):
    """Simplify a name for sorting purposes."""
    for (original, replacement) in SIMPLIFY_CHARS:
        name = name.replace(original, replacement)
    return name.lower()


if __name__ == "__main__":
    main()
