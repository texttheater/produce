#!/usr/bin/env python

"""Input: CoNLL-2000 style labeled file where columns are separated by a single
space, the second-to-last column contains the gold label and the last column
contains the predicted label. Output: a confusion matrix."""

from __future__ import division

import sys
import tables

from collections import OrderedDict, Counter

def mapf(function):
    return lambda x: map(function, x)

def compose(f1, f2):
    return lambda x: f2(f1(x))

count = 0
errors = 0
matrix = {}

# Read and count

for line in sys.stdin:
    line = line.rstrip()
    if not line:
       continue
    fields = line.split(' ')
    gold = fields[-2]
    predicted = fields[-1]
    count += 1
    if gold != predicted:
        errors += 1
    if not gold in matrix:
        matrix[gold] = {}
    row = matrix[gold]
    if not predicted in row:
        row[predicted] = 0
    row[predicted] = row[predicted] + 1

labels = list(matrix.keys())
freq_by_label = {}

for label in labels:
    freq_by_label[label] = sum(map(int, matrix[label].values()))

sortkey = lambda x: (- freq_by_label[x])
labels.sort(key=sortkey)

# Error rate

print 'Annotated units: %d' % count
print 'Errors:          %d' % errors
print 'Error rate:      %f' % (errors / count)
print

# Confusion matrix

tables.print_table(matrix, rowsortkey=sortkey, columnsortkey=sortkey,
        defaultvalue=0)
print

# Scores for individual labels

countstable = OrderedDict()

for label in labels:
    countstable[label] = Counter()

for gold in labels:
    for predicted in matrix[gold]:
        count = matrix[gold][predicted]
        if gold == predicted:
            countstable[gold]['tp'] += count
        else:
            countstable[gold]['fn'] += count
            countstable[predicted]['fp'] += count

for label in labels:
    counter = countstable[label]
    row = OrderedDict(counter)
    countstable[label] = row
    for m in ('tp', 'fn', 'fp'):
        if m not in row:
            row[m] = 0
    try:
        row['prec'] = row['tp'] / (row['tp'] + row['fp'])
    except ZeroDivisionError:
        row['prec'] = 'N/A'
    try:
        row['rec'] = row['tp'] / (row['tp'] + row['fn'])
    except ZeroDivisionError:
        row['rec'] = 'N/A'
    try:
        row['f1'] = 2 * row['prec'] * row['rec'] / (row['prec'] + row['rec'])
    except TypeError:
        row['f1'] = 'N/A'

tables.print_table(countstable)

