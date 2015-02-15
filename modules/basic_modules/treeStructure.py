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
        self.depth = None

    def __str__(self):
        return str(self.__dict__)


class Branch:
    """
    a branch represents a relation (mostly parent-child) between two leaves
    """

    def __init__(self, leaf1, leaf2):
        self.source = {'level': leaf1.level, 'order': leaf1.order, 'unique_key': leaf1.unique_key}
        self.target = {'level': leaf2.level, 'order': leaf2.order, 'unique_key': leaf2.unique_key}
        self.color = "black"

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
        self.leaves.append(leaf)
        self.columns[leaf.level] = self.columns.get(leaf.level, []) + [leaf]

        return leaf

    def add_branch(self, branch):
        for leaf in self.leaves:
            if branch.source['unique_key'] == leaf.unique_key:
                branch.source['order'] = leaf.order
                branch.source['level'] = leaf.level
            if branch.target['unique_key'] == leaf.unique_key:
                branch.target['order'] = leaf.order
                branch.target['level'] = leaf.level

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
                                self.leaves.remove(leaf2)
                                self.columns[level].remove(leaf2)

                                for branch in self.branches:

                                    if branch.source['unique_key'] == leaf2.unique_key:
                                        branch.source['order'] = leaf1.order
                                        branch.source['level'] = leaf1.level
                                        branch.source['unique_key'] = leaf1.unique_key

                                    if branch.target['unique_key'] == leaf2.unique_key:
                                        branch.target['order'] = leaf1.order
                                        branch.target['level'] = leaf1.level
                                        branch.target['unique_key'] = leaf1.unique_key

    def merge_between_columns(self):
        for level1 in sorted(self.columns.keys()):  # for each column
            leaf_list_1 = copy.copy(self.columns.get(level1,[]))
            leaf_list_2 = copy.copy(self.columns.get(level1+1,[]))

            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_2):
                    if leaf1.unique_key != leaf2.unique_key:
                        if (string_compare(leaf1.node1['name'] + leaf1.node2['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4\
                                or string_compare(leaf1.node2['name'] + leaf1.node1['name'], leaf2.node1['name'] + leaf2.node2['name'],'LEV') < 4 )\
                                        and len(leaf1.node2['name']) > 2 and len(leaf1.node1['name']) > 2:

                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if leaf2 in self.leaves:
                                self.leaves.remove(leaf2)
                                self.columns[level1+1].remove(leaf2)
                                for branch in self.branches:

                                    if branch.source['unique_key'] == leaf2.unique_key:
                                        branch.source['order'] = leaf1.order
                                        branch.source['level'] = leaf1.level
                                        branch.source['unique_key'] = leaf1.unique_key

                                    if branch.target['unique_key'] == leaf2.unique_key:
                                        branch.target['order'] = leaf1.order
                                        branch.target['level'] = leaf1.level
                                        branch.target['unique_key'] = leaf1.unique_key
                                        self.update_leaf(branch.source['unique_key'], leaf1.level-1)

    def update_leaf(self, unique_key, new_level, new_order=None, shuffle=True):
        leaf_found = False
        for leaf in self.leaves:
            if leaf.unique_key == unique_key:
                self.columns[leaf.level].remove(leaf)

                # we don't like to move nodes to right, so we check if new_level is less that leaf.level
                # if new_level < leaf.level:
                leaf.level = new_level
                # else:
                #     new_level = leaf.level

                if not new_order:
                    if self.columns.get(new_level):
                        new_order = max([leaf2.order for leaf2 in self.columns.get(new_level)])+1
                    else:
                        new_order = 1

                leaf.order = new_order

                self.columns[new_level] = self.columns.get(new_level, []) + [leaf]
                leaf_found = True

        if leaf_found:
            for branch in self.branches:

                if branch.source['unique_key'] == unique_key:
                    branch.source['order'] = new_order
                    branch.source['level'] = new_level

                if branch.target['unique_key'] == unique_key:
                    branch.target['order'] = new_order
                    branch.target['level'] = new_level
                    if shuffle:
                        self.update_leaf(branch.source['unique_key'], new_level-1)


    def remove_vertical_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        :return:
        """
        for level in sorted(self.columns.keys()):
            leaf_list = copy.copy(self.columns.get(level,[]))
            for index, leaf in enumerate(leaf_list):
                self.update_leaf(leaf.unique_key, leaf.level, index+1, False)

    def decrease_depth(self, unique_key, depth):
        for index, leaf in enumerate(self.leaves):
            if leaf.unique_key == unique_key:
                self.leaves[index].depth = depth
                for branch in self.branches:
                    if branch.target['unique_key'] == unique_key:
                        self.decrease_depth(branch.source['unique_key'], depth-1)


    def remove_horizontal_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        :return:
        """
        for index, leaf in enumerate(self.leaves):
            if self.leaves[index].depth is None:
                self.decrease_depth(leaf.unique_key, 0)

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
            self.update_leaf(leaf.unique_key,leaf.depth, None, False)

    def bfs_round(self):
        change_flag = True
        while change_flag:
            change_flag = False
            for leaf_target in self.leaves:
                if leaf_target.depth >= -1:
                    for branch in self.branches:
                        if leaf_target.unique_key == branch.target['unique_key']:
                            for leaf_source in self.leaves:
                                if leaf_source.unique_key == branch.source['unique_key']:
                                    if leaf_source.depth == -3:
                                        leaf_source.depth = leaf_target.depth - 1
                                        change_flag = True

        change_flag = True
        while change_flag:
            change_flag = False
            for leaf_source in self.leaves:
                if leaf_source.depth >= -1:
                    for branch in self.branches:
                        if leaf_source.unique_key == branch.source['unique_key']:
                            for leaf_target in self.leaves:
                                if leaf_target.unique_key == branch.target['unique_key']:
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

