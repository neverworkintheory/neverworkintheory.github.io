#!/usr/bin/env python

import argparse
import glob
from pathlib import Path
import sys

import frontmatter


def main():
    options = get_options()
    for filename in glob.glob(f"{options.root}/**/*.html"):
        post = frontmatter.load(filename)
        if "date" not in post:
            print(f"{filename} has no date")
        actual = post["date"].isoformat()
        expected = "-".join(Path(filename).name.split("-")[:3])
        if actual != expected:
            print(f"{filename}: {actual} internal, {expected} in name")


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", help="root directory")
    return parser.parse_args()


if __name__ == "__main__":
    main()
