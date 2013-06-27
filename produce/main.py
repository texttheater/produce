#!/usr/bin/env python3

import exceptions
import logging
import parse
import sys

logging.basicConfig(level=logging.INFO)

def produce(target, rules):
    for rule in rules:
        if rule.produce(target, rules):
            return

if __name__ == '__main__':
    _, target = sys.argv
    try:
        rules = parse.parse_producefile()
        produce(target, rules)
    except exceptions.UserError as e:
        logging.error(e)
        sys.exit(1)
