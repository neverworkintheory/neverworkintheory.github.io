#!/usr/bin/env python

"""Select and format a single entry."""

import sys
from pybtex.database import parse_string
from pybtex.plugin import find_plugin

key = sys.argv[1]
template = open(sys.argv[2], "r").read()

text = sys.stdin.read()
bib = parse_string(text, "bibtex")

if key not in bib.entries:
    print(f"Key {key} not found", file=sys.stderr)
    sys.exit(1)

html = find_plugin("pybtex.backends", "html")()
style = find_plugin("pybtex.style.formatting", "unsrt")()
formatted = style.format_bibliography(bib)
citation = [entry.text.render(html) for entry in formatted if entry.key == key][0]
abstract = bib.entries[key].fields["abstract"]

print(template.format(key=key, citation=citation, abstract=abstract))
