import sys

def list_union(lists):
    result = []
    seen = set()
    for l in lists:
        for element in l:
            if not element in seen:
                result.append(element)
                seen.add(element)
    return result

def isnumber(x):
    return isinstance(x, (int, long, float, complex))

def out(string):
    sys.stdout.write('%s' % string)

def nl():
    out('\n')
