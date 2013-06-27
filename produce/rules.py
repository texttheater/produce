import errno
import main
import re
import string

variable_pattern = re.compile(r'\$\{([A-Za-z0-9-_])+\}')

class Rule:

    def __init__(self, atts, line):
        self.atts = atts
        self.line = line
        # Process target:
        if not 'target' in atts:
            raise ProducefileError(line, 'rule has no target attribute')
        self.target_pattern = parse_target(atts['target'], line)
        # Process prerequisites:
        self.prereqs = []
        for key, value in atts.items():
            if key.startswith('prereq'): # TODO allow multi-valued attributes to avoid having to name them differently?
                self.prereqs.append(value)
        # Process recipe:
        if not 'recipe' in atts:
            raise ProducefileError(line, 'rule has no recipe attribute')
        self.recipe = atts['recipe']

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
        return InstantiatedRule(target, new_atts, self)

class InstantiatedRule:

    def __init__(self, target, atts, rule):
        self.target = target
        self.atts = atts
        self.rule = rule

    def produce(self, rules):
        prereqs = map(self.instantiate_pattern, self.rule.prereqs)
        for prereq in prereqs:
            main.produce(prereq, rules) # TODO need a more intelligent algorithm so we can delete intermediate targets
        if not up_to_date(self.target, prereqs):
            recipe = self.instantiate_pattern(rule.recipe)
            subprocess.call(recipe, shell=True) # TODO specify which shell
            if not up_to_date(self.target, prereqs):
                raise ProducefileError(self.rule.line,
                        'recipe failed to update %s' % self.target)

    def instantiate_pattern(pattern):
        template = string.Template(pattern)
        return template.substitute(self.atts)

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

def up_to_date(target, prereqs):
    try:
        tstat = os.stat(target)
    except OSError, e:
        if e.errno == errno.ENOENT:
            return False
        raise UserError('cannot stat %s [Errno %d]' % (target, e.errno))
    for prereq in prereqs:
        try:
            pstat = os.stat(prereq)
        except OSError, e:
            if e.errno == errno.ENOENT:
                continue
            raise UserError('cannot stat %s [Errno %d]' % (prereq, e.errno))
        if pstat.mtime > tstat.mtime: # TODO is this precise enough?
            return False
    return True
