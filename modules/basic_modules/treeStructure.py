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

    def __init__(self, node1, node2, doc_id, date, level=-1, color="beige"):
        self.node1 = node1.__dict__
        self.node2 = node2.__dict__
        self.level = level
        self.order = -1
        self.depth = None
        self.color = color
        self.doc_id = str(doc_id)
        self.min_date = int(date[-4:])
        self.max_date = int(date[-4:])
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

        leaf.index = len(self.leaves) + 1
        self.leaves.append(leaf)
        self.columns[leaf.level] = self.columns.get(leaf.level, []) + [leaf]



        return leaf

    def merge_leaf(self, main_leaf, to_be_removed_leaf):
        # if to_be_removed_leaf.index == 293:
        #     print 'found!', to_be_removed_leaf.node1['name'], to_be_removed_leaf.node2['name']
        #     for branch in self.branches:
        #         if branch.source == to_be_removed_leaf.index:
        #             branch.source = 1
        #
        #         if branch.target == to_be_removed_leaf.index:
        #             branch.source = 1

        if main_leaf.index == 293:
            # print 'found! found!!', to_be_removed_leaf.node1['name'], to_be_removed_leaf.node2['name']
            for branch in self.branches:
                if branch.source == to_be_removed_leaf.index:
                    branch.source = 1

                if branch.target == to_be_removed_leaf.index:
                    branch.source = 1


        self.leaves.remove(to_be_removed_leaf)
        self.columns[to_be_removed_leaf.level].remove(to_be_removed_leaf)

        for branch in self.branches:

            if branch.source == to_be_removed_leaf.index:
                branch.source = main_leaf.index

            if branch.target == to_be_removed_leaf.index:
                branch.target = main_leaf.index


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
        return {'leaves': [leaf.__dict__ for leaf in self.leaves],
                'branches': [branch.__dict__ for branch in self.branches]}

    def update(self):
        self.merge_columns()
        self.remove_horizontal_gaps()
        self.merge_columns_for_births()
        self.remove_vertical_gaps()

    def merge_columns(self):

        for level in sorted(self.columns.keys()):  # for each column
            leaf_list_1 = copy.copy(
                self.columns[level])  # take a copy of all leaves such that you don't mix things up between the levels.
            leaf_list_2 = copy.copy(self.columns.get(level + 1, []))
            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_1):
                    if index2 > index1:
                        if (string_compare(leaf1.node1['name'] + leaf1.node2['name'],
                                           leaf2.node1['name'] + leaf2.node2['name'], 'LEV') < 4 \
                                    or string_compare(leaf1.node2['name'] + leaf1.node1['name'],
                                                      leaf2.node1['name'] + leaf2.node2['name'], 'LEV') < 4 ) \
                                and len(leaf1.node2['name']) > 2 and len(leaf1.node1['name']) > 2:
                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if leaf2 in self.leaves and leaf1 in self.leaves:
                                leaf1.doc_id += ', ' + leaf2.doc_id
                                if leaf2.min_date < leaf1.min_date:
                                    leaf1.min_date = leaf2.min_date
                                if leaf2.max_date > leaf1.max_date:
                                    leaf1.max_date = leaf2.max_date

                                self.merge_leaf(leaf1, leaf2)


            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_2):
                    if leaf1.index != leaf2.index:
                        if (string_compare(leaf1.node1['name'] + leaf1.node2['name'],
                                           leaf2.node1['name'] + leaf2.node2['name'], 'LEV') < 4 \
                                    or string_compare(leaf1.node2['name'] + leaf1.node1['name'],
                                                      leaf2.node1['name'] + leaf2.node2['name'], 'LEV') < 4 ) \
                                and len(leaf1.node2['name']) > 2 and len(leaf1.node1['name']) > 2:

                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if leaf2 in self.leaves and leaf1 in self.leaves:

                                leaf1.doc_id += ', ' + leaf2.doc_id
                                if leaf2.min_date < leaf1.min_date:
                                    leaf1.min_date = leaf2.min_date
                                if leaf2.max_date > leaf1.max_date:
                                    leaf1.max_date = leaf2.max_date

                                self.merge_leaf(leaf1, leaf2)
                                #
                                # for branch in self.branches:
                                #     if branch.target == leaf1.index:
                                #         self.update_leaf(branch.source, leaf1.level - 1)

    def get_ancestors(self, index):
        source_list = []
        for branch in self.branches:
            if branch.target == index:
                source_list.append(branch.source)
        return source_list


    def merge_columns_for_births(self):
        for level in sorted(self.columns.keys()):  # for each column
            leaf_list_1 = copy.copy(self.columns[level])

            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_1):
                    if index2 > index1:
                        # to capture the '- x' for birth and '- ' for death
                        if (len(leaf1.node2['name']) < 3 or len(leaf2.node2['name']) < 2) and \
                                (string_compare(leaf1.node1['name'], leaf2.node1['name'],'LEV') < 3 or
                                 string_compare(leaf1.node1['name'], leaf2.node2['name'],'LEV') < 3 or
                                 string_compare(leaf1.node2['name'], leaf2.node1['name'],'LEV') < 3):

                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if len(leaf2.node2['name']) < 3:  # leaf1 += leaf2
                                if set(self.get_ancestors(leaf1.index)).intersection(self.get_ancestors(leaf2.index)):

                                    if leaf2 in self.leaves and leaf1 in self.leaves:
                                        leaf1.doc_id += ', ' + leaf2.doc_id
                                        if leaf2.min_date < leaf1.min_date:
                                            leaf1.min_date = leaf2.min_date
                                        if leaf2.max_date > leaf1.max_date:
                                            leaf1.max_date = leaf2.max_date

                                        self.merge_leaf(leaf1, leaf2)

            # to merge the lower leaf with and upper one
            for index1, leaf1 in enumerate(leaf_list_1):
                for index2, leaf2 in enumerate(leaf_list_1):
                    if index2 < index1:
                        # to capture the '- x' for birth and '- ' for death
                        if (len(leaf1.node2['name']) < 3 or len(leaf2.node2['name']) < 2) and \
                                (string_compare(leaf1.node1['name'], leaf2.node1['name'],'LEV') < 3 or
                                 string_compare(leaf1.node1['name'], leaf2.node2['name'],'LEV') < 3 or
                                 string_compare(leaf1.node2['name'], leaf2.node1['name'],'LEV') < 3):

                            # here we want to remove leaf2 and redirect every pointer to leaf1
                            if len(leaf2.node2['name']) < 3:  # leaf1 += leaf2
                                if set(self.get_ancestors(leaf1.index)).intersection(self.get_ancestors(leaf2.index)):

                                    if leaf2 in self.leaves and leaf1 in self.leaves:
                                        leaf1.doc_id += ', ' + leaf2.doc_id
                                        if leaf2.min_date < leaf1.min_date:
                                            leaf1.min_date = leaf2.min_date
                                        if leaf2.max_date > leaf1.max_date:
                                            leaf1.max_date = leaf2.max_date

                                        self.merge_leaf(leaf1, leaf2)


    def update_leaf(self, index, new_level, new_order=None, shuffle=True):
        leaf_found = False
        for leaf in self.leaves:
            if leaf.index == index:
                self.columns[leaf.level].remove(leaf)

                # we don't like to move nodes to right, so we check if new_level is less that leaf.level
                leaf.level = new_level

                if not new_order:
                    if self.columns.get(new_level):
                        new_order = max([leaf_tmp.order for leaf_tmp in self.columns.get(new_level)]) + 1
                    else:
                        new_order = 1

                leaf.order = new_order

                self.columns[new_level] = self.columns.get(new_level, []) + [leaf]
                leaf_found = True

        if leaf_found:
            for branch in self.branches:
                if branch.target == index:
                    if shuffle:
                        self.update_leaf(branch.source, new_level - 1)

    def remove_vertical_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        :return:
        """
        for level in sorted(self.columns.keys()):
            leaf_list = copy.copy(self.columns.get(level, []))

            # sorting the leaves based on average date.
            # data = [((l.min_date + l.max_date) / 2, l) for l in leaf_list]
            data = [(l.min_date, l) for l in leaf_list]
            data = sorted(data, key=itemgetter(0))

            for index_tmp, leaf in enumerate(data):
                self.update_leaf(leaf[1].index, leaf[1].level, index_tmp + 1, False)

    def decrease_depth(self, index, depth):
        for index_tmp, leaf in enumerate(self.leaves):
            if leaf.index == index and (leaf.depth is None or leaf.depth >= depth):
                self.leaves[index_tmp].depth = depth
                for branch in self.branches:
                    if branch.target == index:
                        self.decrease_depth(branch.source, depth - 1)

    def remove_horizontal_gaps(self):
        """
        here we sort all the nodes in each column based on their index.
        """
        for index_tmp, leaf in enumerate(self.leaves):
            if self.leaves[index_tmp].depth is None:
                self.decrease_depth(leaf.index, 0)

        max_depth = 10
        for leaf in self.leaves:
            if leaf.depth < max_depth:
                max_depth = leaf.depth

        for leaf in self.leaves:
            if not leaf.depth == max_depth:
                leaf.depth = -4
            else:
                leaf.depth = -1

        self.bfs_round()
        self.bfs_round()
        self.bfs_round()
        self.bfs_round()

        for leaf in self.leaves:
            self.update_leaf(leaf.index, leaf.depth, None, False)

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
                                    if leaf_source.depth == -4:
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

