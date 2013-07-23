#!/usr/bin/env python

import sys
import re
import yaml

item_p = re.compile(r'<item>(.+?)</item>', re.DOTALL)
post_name_p = re.compile(r'<wp:post_name>(.+)</wp:post_name>')
post_date_p = re.compile(r'<wp:post_date>(.+)</wp:post_date>')
content_p = re.compile(r'<content:encoded><!\[CDATA\[(.+)\]\]></content:encoded>', re.DOTALL)
author_p = re.compile(r'<dc:creator>(.+)</dc:creator>')
title_p = re.compile(r'<title>(.+)</title>')
link_p = re.compile(r'<link>(.+)</link>')
category_p = re.compile(r'<category domain="category" nicename="[^"]+"><!\[CDATA\[(.+)\]\]></category>')

authors = {
    'jorge' : 'Jorge Aranda',
    'gvwilson' : 'Greg Wilson',
    'neil' : 'Neil Ernst',
    'ChristophTreude' : 'Christoph Treude',
    'LeifSinger' : 'Leif Singer',
    'AndreasStefik' : 'Andreas Stefik',
    'FelienneHermans' : 'Felienne Hermans',
    'Fayola Peters' : 'Fayola Peters'
}

data = sys.stdin.read()
for item in item_p.findall(data):
    if '<wp:post_type>post</wp:post_type>' not in item:
        continue
    name = post_name_p.search(item).group(1)
    post_date = post_date_p.search(item).group(1)
    date, time = post_date.split(' ')
    year, month, day = date.split('-')
    content = content_p.search(item).group(1)
    author = authors[author_p.search(item).group(1)]
    title = title_p.search(item).group(1)
    categories = category_p.findall(item)
    link = link_p.search(item).group(1)
    pathname = '_posts/%s-%s-%s-%s.html' % (year, month, day, name)
    print link, ':', '%s/%s/%s/%s.html' % (year, month, day, name)
    with open(pathname, 'w') as writer:
        print >> writer, '---'
        print >> writer, 'layout: post'
        print >> writer, 'author:', author
        print >> writer, 'title: "%s"' % title
        print >> writer, 'date:', date
        print >> writer, 'time:', time
        print >> writer, 'categories: [%s]' % ', '.join(categories)
        print >> writer, '---'
        print >> writer
        print >> writer, content.strip()
