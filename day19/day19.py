class WorkflowRule:
    def __init__(self, operator, compare_val, target, operand):
        self.operator = operator
        self.compare_val = compare_val
        self.target_workflow = target
        self.operand = operand

    def matches(self, item):
        # Last rule without a target always matches
        if self.operand is None:
            return True
        if self.operand == '>':
            if item.vals[self.operator] > int(self.compare_val):
                return True
        elif self.operand == '<':
            if item.vals[self.operator] < int(self.compare_val):
                return True
        return False

    def __repr__(self):
        return f'Rule: {self.operator} {self.compare_val} {self.target_workflow}'

class Workflow:
    def __init__(self, name, rules, special):
        self.rules = rules
        self.name = name
        self.special = special

    def capture_item(self, item):
        item.associated_workflow = self.name

    def __repr__(self):
        return f'Workflow: {self.name} Rules: {self.rules} Active Items: {len(self.active_items)}'

class Item:
    def __init__(self, vals):
        self.vals = vals
        self.associated_workflow = None

    def __repr__(self) -> str:
        return f"x: {self.vals['x']} m: {self.vals['m']} a: {self.vals['a']} s: {self.vals['s']} in {self.associated_workflow}"

def parse_workflow_rules(line):
    # Example line: px{a<2006:qkq,m>2090:A,rfg}
    parts = line.split('{')
    workflow_name = parts[0]
    parts = parts[1].split('}')[0]
    rule_strings = parts.split(',')
    rules = []
    for rule in rule_strings:        
        operator = None
        compare_val = None
        operand = None
        if ':' in rule:
            name_parts = rule.split(':')
            target = name_parts[1]
            rule_parts = name_parts[0].split('>')
            operand = '>'
            if len(rule_parts) == 1:
                rule_parts = name_parts[0].split('<')
                operand = '<'
            operator = rule_parts[0]
            compare_val = rule_parts[1]
        else:
            target = rule
        rules.append(WorkflowRule(operator, compare_val, target, operand))
    return Workflow(workflow_name, rules, False)



lines = [l.strip() for l in open('Inputs/day19.txt').readlines() if l.strip() != '']

items = []
workflows = {}
for l in lines:
    if l.startswith('{'):
        to_parse = l[1:-1]
        item_values = [x.split('=') for x in to_parse.split(',')]
        item_value_dict = {x[0]: int(x[1]) for x in item_values}
        items.append(Item(item_value_dict))
    else:
        workflow = parse_workflow_rules(l)
        workflows[workflow.name] = workflow

workflows['A'] = Workflow('A', [], True)
workflows['R'] = Workflow('R', [], True)

# First pass - add items to the in workflow
for i in items:
    workflows["in"].capture_item(i)

continue_processing = True
while continue_processing:
    continue_processing = False
    for i in items:
        w = workflows[i.associated_workflow]
        if w.special:
            continue
        continue_processing = True
        for r in w.rules:
            if r.matches(i):
                workflows[r.target_workflow].capture_item(i)
                break

print("Part 1:", sum([sum(i.vals.values()) for i in items if i.associated_workflow == 'A']))


def terminal_paths(workflows, start_at):
    result = []
    if workflows[start_at].special:        
        return [[(start_at, None, None, None, None)]]
    rules = workflows[start_at].rules
    not_rules = []
    for r in rules:        
        for t in terminal_paths(workflows, r.target_workflow):
            result.append([(start_at, r.target_workflow, r.operand, r.compare_val, r.operator, '')] + not_rules + t)
        not_rules.append((start_at, r.target_workflow, r.operand, r.compare_val, r.operator, 'not'))
    return result

terminuses = terminal_paths(workflows, 'in')
accept_terminuses = [terminus for terminus in terminuses if terminus[-1][0] == 'A']

def filter_match(filter_list):    
    if len(filter_list) == 0:
        return 4000
    return_val = 0
    filter = ' and '.join(filter_list)
    for check_val in range(1, 4001):
        if eval(filter.replace('x', str(check_val))):
            return_val += 1
    return return_val

possible_values = 0
for term in accept_terminuses:
    # We start with all possible values falling through the path    
    current_filters = {'x': [], 'm': [], 'a': [], 's': []}
    # Each rule will reduce the number of possible values that can satisfy it
    for rule in term:
        # A redirect rule (with no filter) has no effect on the possible values
        if rule[2] is None:
            continue
        if (rule[2] == '>' and rule[5] != 'not') or (rule[2] == '<' and rule[5] == 'not'):
            local_op = '>'
            if rule[5] == "not":
                local_op += '='
            current_filters[rule[4]].append("x" + local_op + rule[3])
        elif (rule[2] == '<' and rule[5] != 'not') or (rule[2] == '>' and rule[5] == 'not'):
            local_op = '<'
            if rule[5] == "not":
                local_op += '='
            current_filters[rule[4]].append("x" + local_op + rule[3])
    candidate = filter_match(current_filters['x']) * filter_match(current_filters['m']) * filter_match(current_filters['a']) * filter_match(current_filters['s'])
    if (candidate > 0):
        possible_values += candidate


print("Part 2:", possible_values)
