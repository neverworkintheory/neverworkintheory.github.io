"""Convert bibliography to HTML suitable for inclusion."""

import argparse

from pybtex.database import parse_string
from pybtex.plugin import find_plugin

BIBTEX_STYLE = "unsrt"


def main():
    config = _parse_args()
    bib = _read_bib(config.bib, config.strings)
    html = find_plugin("pybtex.backends", "html")()

    entries = [_format(entry.key, entry.text.render(html)) for entry in bib]
    result = "<dl>\n\n" + "\n\n".join(entries) + "\n\n</dl>"

    writer = open(config.output, "w") if config.output else sys.stdout
    writer.write(result)


def _format(key, body):
    """Format a single bibliography entry."""
    return f'<dt id="{key}">{key}</dt>\n<dd>{body}</dd>'


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--bib", help="Bibliography BibTeX file")
    parser.add_argument("--output", help="Output file", default=None)
    parser.add_argument("--strings", help="String definitions BibTeX file")
    return parser.parse_args()


def _read_bib(bib_path, strings_path):
    """Read bibliography, formatting on the way."""
    strings = open(strings_path, "r").read()
    bib = open(bib_path, "r").read()
    bib = strings + "\n\n" + bib
    bib = parse_string(bib, "bibtex")
    style = find_plugin("pybtex.style.formatting", BIBTEX_STYLE)()
    return style.format_bibliography(bib)


if __name__ == "__main__":
    main()
