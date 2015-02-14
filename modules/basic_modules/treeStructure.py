import uuid

__author__ = 'bijan'


class LeafNode:
    """
    a leaf node is basically a single person who forms a leaf by coupling to another person
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.namenew


class Leaf:
    """
    a leaf represents a couple. Each lever has an order and a level which shows where it is positioned
    """

    def __init__(self, node1, node2, level=0, order=0):
        self.node1 = node1.__dict__
        self.node2 = node2.__dict__
        self.level = level
        self.order = order
        self.unique_key = uuid.uuid4()

    def __str__(self):
        return str(self.__dict__)

class Branch:
    """
    a branch represents a relation (mostly parent-child) between two leaves
    """

    def __init__(self, leaf1, leaf2):
        self.source = {'level': leaf1.level, 'order': leaf1.order, 'unique_key': leaf1.unique_key}
        self.target = {'level': leaf2.level, 'order': leaf2.order, 'unique_key': leaf2.unique_key}

    def __str__(self):
        return str(self.source) + str(self.target)


class TreeStructure:
    def __init__(self):
        self.leaves = []
        self.branches = []
        self.columns = {}

    def add_leaf(self, leaf):

        if leaf.order <= len(self.columns.get(leaf.level,[])):
            leaf.order += 1
        self.leaves.append(leaf.__dict__)
        self.columns[leaf.level] = self.columns.get(leaf.level, []) + [leaf.__dict__]

        return leaf

    def add_branch(self, branch):
        for leaf in self.leaves:
            print branch.__dict__
            if branch.source['unique_key'] == leaf['unique_key']:
                branch.source['order'] = leaf['order']
                branch.source['level'] = leaf['level']
            if branch.target['unique_key'] == leaf['unique_key']:
                branch.target['order'] = leaf['order']
                branch.target['level'] = leaf['level']

        self.branches.append(branch.__dict__)



if __name__ == "__main__":
    tree = TreeStructure()
    lnode1 = LeafNode('Adriaan Made')
    lnode2 = LeafNode('Lijntje Timmers')
    lnode3 = LeafNode('Govert Sneep')
    lnode4 = LeafNode('Jacoba Bezooijen')
    lnode5 = LeafNode('Jacobus Sneep')
    lnode6 = LeafNode('-')
    lnode7 = LeafNode('Stijntje Made')

    leaf1 = Leaf(lnode1,lnode2,1,1)
    leaf2 = Leaf(lnode3,lnode4,1,2)
    leaf3 = Leaf(lnode1,lnode2,1,3)
    leaf4 = Leaf(lnode5,lnode6,2,1)
    leaf5 = Leaf(lnode5,lnode7,2,2)

    branch1 = Branch(leaf1,leaf4)
    branch2 = Branch(leaf2,leaf5)
    branch3 = Branch(leaf3,leaf5)

    tree.add_leaf(leaf1)
    tree.add_leaf(leaf2),tree.add_leaf(leaf3),tree.add_leaf(leaf4),tree.add_leaf(leaf5)
    tree.add_branch(branch1),tree.add_branch(branch2),tree.add_branch(branch3)

    visualize_tree(tree)
