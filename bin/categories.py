#!/usr/bin/env python

"""
Display all the categories used in blog posts.
"""

import sys
import re

cat_p = re.compile('categories:\s*\[(.+)\]')

categories = set()
for filename in sys.argv[1:]:
    with open(filename, 'r') as reader:
        data = reader.read()
    m = cat_p.search(data)
    assert m, "No categories match for %s" % filename
    categories.update([x.strip() for x in m.group(1).split(',')])
for c in sorted(categories):
    print c
