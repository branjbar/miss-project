"""
    This code builds a huge graph in which each node is an individual and edges are either because of family relations
     or blocking keys.

At the end the exported csv file can be imported in mysql using:
    LOAD DATA INFILE '/Users/Bijan/sandbox/Eclipse_Projects/linkPy/data/matching_kdd/matches_random_walk_100.csv'
    INTO TABLE miss_matches_random_walk FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';


"""
import matplotlib

matplotlib.use('TkAgg')
import networkx
import operator
import time
import math
from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.dynak.visualize import get_family_edge
from modules.basic_modules.random_walk import get_proximity, RandomWalk
import os
import heapq  # for finding the k largest element

FILE_NAME = "../../../data/matching_random_walk/matches_random_walk_%d.csv"

MAX_BLOCK_SIZE = 30  # the maximum block size which is acceptable


class EntityResolution():
    def __init__(self):

        self.block_dict = {}  # block_dict = {block_id: [ref1_id, ref2_id, ...]}
        self.document_dict = {}  # document_dict = {document_id: [ref1_id, ref2_id, ...]}
        self.reference_dict = {}  # reference_dict = {ref_id: document_id}

        self.graph = networkx.Graph()  # a graph, nodes: references and blocks, edges: family relations and block membership
        self.random_walk = None

    def load_dictionary(self, from_file=False, limit=1000):
        """
            loads the required dictionaries that contain useful information about blocks and documents


        """
        if not from_file:

            log("start gathering blocks and documents")


            # let's keep it as light as possible
            block_query = """
                            SELECT id, block_id, register_id
                            FROM links_based.all_persons_new
                            LIMIT %d
                          """ % limit
            cur = basic.run_query(block_query)

            for c in cur.fetchall():
                ref_id = c[0]
                block_id = c[1]
                register_id = c[2]
                self.reference_dict[ref_id] = register_id
                if block_id != 1888:
                    self.block_dict[block_id] = self.block_dict.get(block_id, []) + [ref_id]
                self.document_dict[register_id] = self.document_dict.get(register_id, []) + [ref_id]

    def load_graph(self):
        """
            generates a graph from the dictionaries
            """
        log("start building the graph based on blocks")

        # add block edges first
        for block_id in self.block_dict.keys():
            ref_list = self.block_dict[block_id]
            if len(ref_list) < MAX_BLOCK_SIZE:  # to avoid huge graphs for now
                for ref1 in ref_list:
                    for ref2 in ref_list:
                        if ref2 > ref1:
                            self.graph.add_node(ref1, block_id=block_id)
                            self.graph.add_node(ref2, block_id=block_id)
                            self.graph.add_edge(ref1, ref2)

        log("start adding the family relations")

        for node in self.graph.nodes():
            edge_list = get_family_edge(self.document_dict[self.reference_dict[node]])
            for e in edge_list:
                self.graph.add_edge(e[0], e[1])

    def get_similars(self, reference, restart=.3):
        """
        """
        similarity_list = []
        if not self.random_walk:
            self.random_walk = RandomWalk(self.graph)

        self.random_walk.generate_x_initial([reference])
        self.random_walk.run_uniform(restart)
        k_keys_sorted_by_values = heapq.nlargest(10, self.random_walk.proximity_dict,
                                                 key=self.random_walk.proximity_dict.__getitem__)
        # here the problem is that many of the similar nodes are not acceptable:
        #   * being equal to the reference
        #   * being in the same document as the reference
        #   * not being in the same block as reference
        #   * some returned similars have a proximity of zero

        for key in k_keys_sorted_by_values:
            if not key == reference \
                    and self.graph.node[reference].get('block_id') == self.graph.node[key].get('block_id') \
                    and (reference - key > 3 or reference - key < -3)\
                    and self.random_walk.proximity_dict[key]>0:
                similarity_list.append([key, self.random_walk.proximity_dict[key]])

        return similarity_list


def main():
    entity_resolution = EntityResolution()
    entity_resolution.load_dictionary(False, 1000)
    entity_resolution.load_graph()

    for node in entity_resolution.graph.nodes():
        similars_list = entity_resolution.get_similars(node)
        print 'random walk for %d' % node, similars_list


if __name__ == "__main__":
    main()


