"""
Everything to do with parsing the Producefile goes here.
"""

import exceptions
import itertools
import re
import rules

key_value_pattern = re.compile(r'^([A-Za-z0-9-_]): +(.*)$')

def parse_producefile():
    """
    Looks for the Producefile in the present working directory. Returns
    its rules as a list of Rule objects.
    """
    try:
        with open('Producefile') as f:
            return map(rule, blocks(f))
    except IOError, e:
        raise exceptions.UserError('Could not read Producefile: %s' % e)

class Block:

    def __init__(self, first_line, lines):
        self.first_line = first_line
        self.lines = lines

def blocks(f):
    lines = []
    line = 0
    for line in itertools.chain(f, ''):
        line +=1
        line = line.rstrip()
        if line.startswith('#'): # comment
            continue
        if line:
            lines.append(line)
        else:
            if lines:
                yield Block(line - len(lines), lines)
                lines = []

def rule(block):
    atts = {}
    for i, line in enumerate(block.lines):
        match = key_value_pattern.match(line)
        if not match:
            raise exceptions.ProducefileError(block.first_line + i,
                    'cannot parse line')
        key = match.group(1)
        value = match.group(2)
        result[key] = value
    return rules.Rule(atts, block.first_line)
