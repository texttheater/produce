#!/usr/bin/env python

"""Expand natural language inspired templates to Wapiti patterns."""

import re
import sys

# This is our little template language. It allows to name feature columns and
# to extract n-grams in windows centered around the current item.
naming_pattern = re.compile(r'feature (\d)+ = (.+)')
ngrams_pattern = re.compile(r'(.+) (uni|bi|tri|\d+-)grams in width-(\d+) window')

def expand(inline):
    match = naming_pattern.match(inline)
    if match:
        return expand_naming(match)
    match = ngrams_pattern.match(inline)
    if match:
        return expand_ngrams(match)
    return [inline]

def expand_naming(match):
    feature_number = match.group(1)
    feature_name = match.group(2)
    features[feature_name] = feature_number
    return []

def prefix2arity(prefix):
    if prefix == 'uni':
        return 1
    if prefix == 'bi':
        return 2
    if prefix == 'tri':
        return 3
    return int(prefix[:-1])

def offset2mnemonic(offset, width):
    if offset == 0:
        c = 'X'
        cnum = 1
    elif offset < 0:
        c = 'L'
        cnum = abs(offset)
    else:
        c = 'R'
        cnum = offset
    snum = width / 2 - cnum
    return c * cnum + ' ' * snum

def macros(offset, arity, feature_number):
    return '/'.join(macro_list(offset, arity, feature_number))

def macro_list(offset, arity, feature_number):
    for i in range(arity):
       yield '%%X[%s,%s]' % (offset + i, feature_number)

def expand_ngrams(match):
    yield '# ' + match.group(0)
    feature_name = match.group(1)
    arity = prefix2arity(match.group(2))
    width = int(match.group(3))
    number_ngrams = width - arity + 1
    feature_number = features[feature_name]
    if width % 2 == 0:
        raise Exception('width must be odd')
    for i in xrange(number_ngrams):
        offset = i - width / 2
        yield 'U:%s-%s%s=%s' % (feature_name, arity,
                offset2mnemonic(offset, width),
                macros(offset, arity, feature_number))
    yield ''

features = {}

for inline in sys.stdin:
    inline = inline.rstrip()
    for outline in expand(inline):
        print outline
