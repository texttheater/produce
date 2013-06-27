import main
import re

variable_pattern = re.compile(r'\$\{([A-Za-z0-9-_])+\}')

class Rule:

    def __init__(self, atts, line):
        self.atts = atts
        self.line = line
        if not 'target' in atts:
            raise ProducefileError(line, 'rule has no target attribute')
        self.target_pattern = parse_target(atts['target'], line)

    def produce(self, target, rules):
        inst = self.instantiate(target)
        if not inst:
            return False
        inst.produce(rules)

    def instantiate(self, target):
        match = self.target_pattern.match(target)
        if not match:
            return None
        new_atts = copy(self.atts)
        new_atts.update(match.groupdict())
        return InstantiatedRule(new_atts)

class InstantiatedRule:

    def __init__(self, target, atts):
        self.atts = atts

    def produce(self, rules):
        pass
        # TODO find out prerequisites by instantiating their patterns
        # TODO recursively produce them
        # TODO find out if target is up to date
        # TODO if not, run recipe

def parse_target(target, line):
    pattern = ''
    while target:
        if target.startswith('$$'):
            pattern = pattern + re.escape('$')
            target = target[2:]
        elif target.startswith('$'):
            match = variable_pattern.match(target)
            if not match:
                raise ProducefileError(line, 'invalid use of $ in target') # TODO find out exact line
            pattern = pattern + '(?P<' + match.group(1) + '>.+)' # no empty matches for now
            target = target[len(match.group(0)):]
        else:
            pattern = pattern + re.escape(target[0])
            target = target[1:]
    return re.compile(pattern)
