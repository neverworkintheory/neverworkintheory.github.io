"""Check PDFs against bibliography."""

import argparse
import glob
import sys

from pybtex.database import parse_string


def main():
    """Main driver."""
    config = _parse_args()

    bib = _read_bib(config.bibs, config.strings)
    unreviewed = _read_unreviewed(config.unreviewed)
    keys = _extract_keys(bib) - unreviewed

    pdfs = _find_pdf(config.pdfdir)
    stems = {_extract_stem(p) for p in pdfs}

    _report("pdf" in config.report, "Missing PDF", keys - stems)
    _report("bib" in config.report, "Missing bib entry", stems - keys)


def _extract_keys(bib):
    """Extract bibliography keys."""
    return set(bib.keys())


def _extract_stem(pdf):
    """Extract stem from PDF filename."""
    if "/" in pdf:
        pdf = pdf.split("/")[-1]
    return pdf.split("-")[0]


def _find_pdf(pdfdir):
    """Find all PDF files."""
    return glob.glob("**/*.pdf", root_dir=pdfdir, recursive=True)


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--bibs", nargs="+", help="Bibliography BibTeX file(s)")
    parser.add_argument("--pdfdir", help="Root directory of PDFs")
    parser.add_argument("--report", nargs="+", default=["bib", "pdf"], help="Missing items to report")
    parser.add_argument("--strings", help="String definitions BibTeX file")
    parser.add_argument("--unreviewed", help="Plaintext file with keys of unreviewed items")
    parser.add_argument("--withbooks", default=False, help="Report missing books")
    return parser.parse_args()


def _read_bib(bib_paths, strings_path):
    """Read bibliography and strings and convert."""
    bib = "\n\n".join(open(b, "r").read() for b in bib_paths)
    strings = open(strings_path, "r").read()
    bib = strings + "\n\n" + bib
    return parse_string(bib, "bibtex").entries


def _read_unreviewed(unreviewed):
    """Read keys of unreviewed bibliography entries."""
    lines = open(unreviewed, "r").readlines()
    lines = [ln.strip() for ln in lines]
    return {ln for ln in lines if ln}


def _report(control, title, keys):
    """Report a problem."""
    if control and keys:
        print(title)
        for k in sorted(keys):
            print(f"- {k}")


if __name__ == "__main__":
    main()
