import copy
from operator import itemgetter
import uuid
from modules.basic_modules.basic import string_compare

__author__ = 'bijan'


class LeafNode:
    """
    a leaf node is basically a single person who forms a leaf by coupling to another person
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Leaf:
    """
    a leaf represents a couple. Each lever has an order and a level which shows where it is positioned
    """

    def __init__(self, node1, node2, doc_id, level=0, order=0):
        self.node1 = node1.__dict__
        self.node2 = node2.__dict__
        self.level = level
        self.order = order
        self.depth = None
        self.doc_id = str(doc_id)
        self.index = -1
        self.unique_key = uuid.uuid4()

    def __str__(self):
        return str(self.__dict__)


class Branch:
    """
    a branch represents a relation (mostly parent-child) between two leaves
    """

    def __init__(self, leaf1, leaf2):
        self.source = leaf1.unique_key
        self.target = leaf2.unique_key
        self.color = "gray"

    def __str__(self):
        return str(self.source) + str(self.target)


class TreeStructure:
    def __init__(self):
        self.leaves = []
        self.branches = []
        self.columns = {}

    def add_leaf(self, leaf):

        if leaf.order <= len(self.columns.get(leaf.level, [])):
            leaf.order = len(self.columns.get(leaf.level, [])) + 1
        leaf.index = len(self.leaves) + 1
        self.leaves.append(leaf)
        self.columns[leaf.level] = self.columns.get(leaf.level, []) + [leaf]

        return leaf

    def add_branch(self, branch):
        for leaf in self.leaves:
            if branch.source == leaf.unique_key:
                branch.source = leaf.index

            if branch.target == leaf.unique_key:
                branch.target = leaf.index

        self.branches.append(branch)

    def get_dict(self):
        """
        generates a dict for json of html page
        """
        return {'leaves':[leaf.__dict__ for leaf in self.leaves],
                'branches':[branch.__dict__ for branch in self.branches]}

    def update(self):
        self.merge_columns()
        self.merge_between_columns()
        self.remove_horizontal_gaps()
        self.remove_vertical_gaps()

    def merge_columns(self):

        for level in sorted(self.columns.keys()):  # for each column
            leaf_list = copy.copy(self.columns[level])  # take a copy of all leaves such that you don't mix things up between the levels.
            for index1, leaf1 in enumerate(leaf_list):
                for index2, leaf2 in enumerate(leaf_list):
                    if index2 > index1:
                        if (string_compare(leaf1.node1['name'] + leaf1.node2['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4\
                                or string_compare(leaf1.node2['name'] + leaf1.node1['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4 )\
                                        and len(leaf1.node2['name']) > 2 and len(leaf1.node1['name']) > 2:
                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if leaf2 in self.leaves:
                                leaf1.doc_id += ', ' + leaf2.doc_id
                                self.leaves.remove(leaf2)
                                self.columns[level].remove(leaf2)

                                for branch in self.branches:

                                    if branch.source == leaf2.index:
                                        branch.source = leaf1.index

                                    if branch.target == leaf2.index:
                                        branch.target = leaf1.index

    def merge_between_columns(self):
        for level1 in sorted(self.columns.keys()):  # for each column
            leaf_list_1 = copy.copy(self.columns.get(level1,[]))
            leaf_list_2 = copy.copy(self.columns.get(level1+1,[]))

            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_2):
                    if leaf1.index != leaf2.index:
                        if (string_compare(leaf1.node1['name'] + leaf1.node2['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4\
                                or string_compare(leaf1.node2['name'] + leaf1.node1['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4 )\
                                        and len(leaf1.node2['name']) > 2 and len(leaf1.node1['name']) > 2:

                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if leaf2 in self.leaves:
                                self.leaves.remove(leaf2)
                                self.columns[level1+1].remove(leaf2)
                                for branch in self.branches:

                                    if branch.source == leaf2.index:
                                        branch.source = leaf1.index

                                    if branch.target == leaf2.index:
                                        branch.target = leaf1.index
                                        self.update_leaf(branch.source, leaf1.level-1)

    def update_leaf(self, index, new_level, new_order=None, shuffle=True):
        leaf_found = False
        for leaf in self.leaves:
            if leaf.index == index:
                self.columns[leaf.level].remove(leaf)

                # we don't like to move nodes to right, so we check if new_level is less that leaf.level
                leaf.level = new_level

                if not new_order:
                    if self.columns.get(new_level):
                        new_order = max([leaf_tmp.order for leaf_tmp in self.columns.get(new_level)])+1
                    else:
                        new_order = 1

                leaf.order = new_order

                self.columns[new_level] = self.columns.get(new_level, []) + [leaf]
                leaf_found = True

        if leaf_found:
            for branch in self.branches:
                if branch.target == index:
                    if shuffle:
                        self.update_leaf(branch.source, new_level-1)


    def remove_vertical_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        :return:
        """
        for level in sorted(self.columns.keys()):
            leaf_list = copy.copy(self.columns.get(level,[]))
            for index_tmp, leaf in enumerate(leaf_list):
                self.update_leaf(leaf.index, leaf.level, index_tmp+1, False)

    def decrease_depth(self, index, depth):
        for index_tmp, leaf in enumerate(self.leaves):
            if leaf.index == index:
                self.leaves[index_tmp].depth = depth
                for branch in self.branches:
                    if branch.target == index:
                        self.decrease_depth(branch.source, depth-1)


    def remove_horizontal_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        :return:
        """
        for index_tmp, leaf in enumerate(self.leaves):
            if self.leaves[index_tmp].depth is None:
                self.decrease_depth(leaf.index, 0)

        MAX_DEPTH = 10
        for leaf in self.leaves:
            if leaf.depth < MAX_DEPTH:
                MAX_DEPTH = leaf.depth


        for leaf in self.leaves:
            if not leaf.depth == MAX_DEPTH:
                leaf.depth = -3
            else:
                leaf.depth = -1

        self.bfs_round()
        self.bfs_round()
        self.bfs_round()
        self.bfs_round()

        for leaf in self.leaves:
            self.update_leaf(leaf.index,leaf.depth, None, False)

    def bfs_round(self):
        change_flag = True
        while change_flag:
            change_flag = False
            for leaf_target in self.leaves:
                if leaf_target.depth >= -1:
                    for branch in self.branches:
                        if leaf_target.index == branch.target:
                            for leaf_source in self.leaves:
                                if leaf_source.index == branch.source:
                                    if leaf_source.depth == -3:
                                        leaf_source.depth = leaf_target.depth - 1
                                        change_flag = True

        change_flag = True
        while change_flag:
            change_flag = False
            for leaf_source in self.leaves:
                if leaf_source.depth >= -1:
                    for branch in self.branches:
                        if leaf_source.index == branch.source:
                            for leaf_target in self.leaves:
                                if leaf_target.index == branch.target:
                                    if leaf_target.depth <= leaf_source.depth:
                                        leaf_target.depth = leaf_source.depth + 1
                                        change_flag = True



if __name__ == "__main__":
    tree = TreeStructure()
    lnode1 = LeafNode('Adriaan Made')
    lnode2 = LeafNode('Lijntje Timmers')
    lnode3 = LeafNode('Govert Sneep')
    lnode4 = LeafNode('Jacoba Bezooijen')
    lnode5 = LeafNode('Jacobus Sneep')
    lnode6 = LeafNode('-')
    lnode7 = LeafNode('Stijntje Made')

    leaf1 = Leaf(lnode1, lnode2, 1, 1)
    leaf2 = Leaf(lnode3, lnode4, 1, 2)
    leaf3 = Leaf(lnode1, lnode2, 1, 3)
    leaf4 = Leaf(lnode5, lnode6, 2, 1)
    leaf5 = Leaf(lnode5, lnode7, 2, 2)

    branch1 = Branch(leaf1, leaf4)
    branch2 = Branch(leaf2, leaf5)
    branch3 = Branch(leaf3, leaf5)

    tree.add_leaf(leaf1)
    tree.add_leaf(leaf2), tree.add_leaf(leaf3), tree.add_leaf(leaf4), tree.add_leaf(leaf5)
    tree.add_branch(branch1), tree.add_branch(branch2), tree.add_branch(branch3)

