from nltk.tree import *
from head_rules import *

def wash(data):
    if '-' in data.label():
        return data.label().split('-')[0]
    else:
        return data.label()


def data_wash(tree):
    try:
        tree.label()
    except AttributeError:
        return tree
    else:
        newlabel = wash(tree)
        newtree = Tree(newlabel, [])
        index = 0
        for subtree in tree:
            newtree.insert(index, data_wash(subtree))
            index = index + 1
        return newtree


def find(tree):
    ans = [wash(tree)]
    for subtree in tree:
        try:
            subtree.label()
        except AttributeError:
            return subtree
        else:
            ans.append(wash(subtree))
    headrules = HeadRules()
    tmp = headrules.check(ans)
    order.append(tmp - 1)
    return find(tree[tmp - 1])


def setlabel(tree, i, label):
    if i == len(order):
        tree.set_label(label)
        return tree
    else:
        newtree = Tree(label, [])
        index = 0
        for subtree in tree:
            if index == order[i]:
                newtree.insert(index, setlabel(subtree, i + 1, label))
            else:
                newtree.insert(index, subtree)
            index = index + 1
        return newtree


def transform(tree, label):
    ans = []
    for subtree in tree:
        try:
            subtree.label()
        except AttributeError:
            return []
        else:
            if subtree.label() == label:
                ans.extend(transform(subtree, label))
            else:
                ans.append(subtree)
    return ans


def root_trans(tree):
    try:
        tree.label()
    except AttributeError:
        return tree
    else:
        global order
        order = []
        x = find(tree)
        tree = setlabel(tree, 0, x)
        subtrees = transform(tree, x)
        index = 0
        newtree = Tree(x, [])
        for subtree in subtrees:
            newtree.insert(index, subtree)
            index = index + 1
        return newtree


def cbt2dep(tree):
    tree = root_trans(tree)
    tmptree = Tree(tree.label(), [])
    index = 0
    for subtree in tree:
        tmptree.insert(index, cbt2dep(subtree))
        index = index + 1
    return tmptree


