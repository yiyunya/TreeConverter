class rule:
    def __init__(self, node):
        self.node = node
        self.rules = []

    def add_rule(self, childs, direction):
        rule = {}
        for child in childs:
            rule[child] = direction
        self.rules.append(rule)

    def add_remainder_rule(self, direction):
        self.rules.append(direction)

    def get_node(self):
        return self.node

    def get_rules(self):
        return self.rules





class HeadRules():
    def __init__(self, dir = './data/chn_headrules.txt'):
        dir = './data/chn_headrules_3.txt'
        rules = open(dir, 'r')
        self.checklist = {}
        for ruleline in rules:
            tokens = ruleline.split()
            linerule = rule(tokens[0])
            direction = tokens[1]
            filter = []
            for token in tokens[2:]:
                if ';' not in token:
                    filter.append(token)
                else:
                    tmp = token.split(';')
                    filter.append(tmp[0])
                    linerule.add_rule(filter, direction)
                    direction = tmp[1]
            linerule.add_remainder_rule(direction)
            self.checklist[tokens[0]] = linerule

    def check(self, nodes):
        node = nodes[0]
        childs = nodes[1:]
        if str(node) in self.checklist:
            noderules = self.checklist[str(node)]
            noderules = noderules.get_rules()
            for rule in noderules:
                if isinstance(rule,dict):
                    filter = []
                    direction = ''
                    i = 1
                    for child in childs:
                        if str(child) in rule:
                            filter.append(i)
                            direction = rule[str(child)]
                        i = i + 1
                    if filter:
                        if direction == 'r':
                            return filter[-1]
                        else:
                            return filter[0]
                else:
                    direction = str(rule)
                    if direction == 'r':
                        return len(nodes)-1
                    else:
                        return 1
        else:
            return len(nodes)-1












