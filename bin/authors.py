#!/usr/bin/env python

"""Construct table of articles by author."""

import sys
from pybtex.database import parse_string

from util import LATEX_CHARS

def main():
    text = sys.stdin.read()
    bib = parse_string(text, "bibtex")
    bib = bib.entries

    unreviewed = {x.strip() for x in open(sys.argv[1], "r").readlines()}

    seen = {}
    for key in sorted(bib.keys()):
        if key in unreviewed:
            continue

        if "reviewed" not in bib[key].fields:
            print(f"entry {key} missing 'reviewed'")
            sys.exit(1)

        reviewed = bib[key].fields["reviewed"]
        for p in bib[key].persons:
            for name in bib[key].persons[p]:
                seen.setdefault(_clean(name), set()).add((key, reviewed))

    print("<table>")
    print('<tr><th>Name</th><th>Citation</th><th>Reviewed</th></tr>')
    for name in sorted(seen.keys(), key=lambda x: _sort(x)):
        first = name
        for (key, reviewed) in sorted(seen[name]):
            _, year, month, day, _ = reviewed.split('/')
            key = f'<a href="/bib/#{key}">{key}</a>'
            reviewed = f'<a href="{{{{\'{reviewed}\' | relative_url}}}}">{year}-{month}-{day}</a>'
            print(f"<tr><td>{first}</td><td>{key}</td><td>{reviewed}</td></tr>")
            first = ""
    print("</table>")


def _clean(name):
    name = str(name)
    for (latex, html) in LATEX_CHARS:
        name = name.replace(latex, html)
    return name


def _sort(name):
    return name.replace("Å", "A").replace("É", "E").replace("Ś", "S").lower()


if __name__ == "__main__":
    main()
