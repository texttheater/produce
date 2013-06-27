#!/usr/bin/env python3

import parse
import sys

def produce(target, rules):
    for rule in rules:
        if rule.produce(target, rules):
            return

if __name__ == '__main__':
    _, target = sys.argv
    rules = parse.parse_producefile()
    produce(target, rules)
