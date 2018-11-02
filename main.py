from nltk.tree import *
from utils import *
from head_rules import *


def addinf(tree):
    subtree = tree[0]
    global num
    try:
        subtree.label()
    except AttributeError:
        num = num + 1
        newtree = Tree(tree.label(), [[subtree, num, tree.label()]])
        return newtree
    else:
        newtree = Tree(tree.label(), [])
        index = 0
        for subtree in tree:
            newtree.insert(index, addinf(subtree))
            index = index + 1
        return newtree


def getoutput(tree, root):
    global output
    x = tree.label()
    pos = x[1]
    x.append(root)
    output[pos - 1] = x
    for subtree in tree:
        getoutput(subtree, pos)


headrules = HeadRules()
textfile = open('./data/ctb.bracketed', encoding='utf-8')
outfile = open('./data/dt.conll', 'w', encoding='utf-8')
for line in textfile:
    if line[0] == '(':
        data = Tree.fromstring(line)
        data = data_wash(data)
        num = 0
        data = addinf(data)
        data = cbt2dep(data)
        output = [[]] * num
        getoutput(data, 0)
        for outputs in output:
            if outputs[3] == 0:
                outfile.write(str(outputs[1]) + '\t' + str(outputs[0]) + '\t_\t_\t' + str(outputs[2]) + '\t_\t' + str(
                    outputs[3]) + '\tROOT\t_\t_' + '\n')
            else:
                outfile.write(str(outputs[1]) + '\t' + str(outputs[0]) + '\t_\t_\t' + str(outputs[2]) + '\t_\t' + str(
                    outputs[3]) + '\tX\t_\t_' + '\n')
        outfile.write('\n')