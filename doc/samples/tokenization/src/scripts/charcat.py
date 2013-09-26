#!/usr/bin/env python

import sys
import unicodedata

for line in sys.stdin:
    line = line.rstrip()
    if line:
        print unicodedata.category(unichr(int(line)))
    else:
        print
