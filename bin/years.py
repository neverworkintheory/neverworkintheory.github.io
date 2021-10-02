#!/usr/bin/env python

from collections import Counter
import argparse
import pandas as pd
import plotly.express as px
import sys

import util


WIDTH = 600
HEIGHT = 300

def main():
    options = get_options()
    entries = util.get_entries(options.strings, options.input)
    years = [int(entry['year']) for entry in entries]
    low, high = min(years), max(years)
    count = Counter(years)
    years = [year for year in range(low, high+1)]
    count = [count[year] if year in count else 0 for year in years]
    df = pd.DataFrame({'year': years, 'count': count})
    fig = px.histogram(df, x='year', y='count',
                       nbins=len(years), width=WIDTH, height=HEIGHT)
    fig.update_layout(xaxis_title='publication year',
                      yaxis_title='count')
    fig.write_image(options.output)


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='specify bibliography file')
    parser.add_argument('--output', help='specify output file')
    parser.add_argument('--strings', help='string definitions file')
    return parser.parse_args()


if __name__ == '__main__':
    main()
