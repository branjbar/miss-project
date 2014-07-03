"""
    This code builds a huge graph in which each node is an individual and edges are either because of family relations
     or blocking keys.

At the end the exported csv file can be imported in mysql using:
    LOAD DATA INFILE '/Users/Bijan/sandbox/Eclipse_Projects/linkPy/data/matching_random_walk/matches_random_walk_10000.csv'
    INTO TABLE miss_matches_random_walk FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';


"""
import matplotlib

matplotlib.use('TkAgg')
import networkx
from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.dynak.visualize import get_family_edge
import os
import heapq  # for finding the k largest element
from modules.basic_modules.random_walk import RandomWalk

FILE_NAME = "../../../data/matching_random_walk/matches_random_walk_%d.csv"

MAX_BLOCK_SIZE = 30  # the maximum block size which is acceptable
MAX_REFERENCES = 500000
DEBUG = False  # if true then does extra prints


class EntityResolution():
    def __init__(self):

        self.block_dict = {}  # block_dict = {block_id: [ref1_id, ref2_id, ...]}
        self.document_dict = {}  # document_dict = {document_id: [ref1_id, ref2_id, ...]}
        self.reference_dict = {}  # reference_dict = {ref_id: document_id}

        self.graph = networkx.Graph()  # a graph. nodes: refs and blocks, edges: family relations and block membership
        self.graphs = []  # a list of graph components
        self.graphs_index = 0  # the index of graph in graphs that is under study
        self.random_walk = None


        # some parameters for exporting message in csv file
        self.export_message = ''  # the message which should be saved in csv file
        self.message_counter = 1
        try: os.remove(FILE_NAME % MAX_REFERENCES)  # to be sure data will not be appended to a non-empty file
        except: pass

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
            block_ref_list = self.block_dict[block_id]
            if len(block_ref_list) < MAX_BLOCK_SIZE:  # to avoid huge graphs for now
                block_node_name = '#block_%d' % block_id
                self.graph.add_node(block_node_name, type="block")
                for reference in block_ref_list:
                    self.graph.add_node(reference, block_id=block_id)
                    self.graph.add_edge(reference, block_node_name)

        log("start adding the family relations")

        for node in self.graph.nodes():
            if not self.graph.node[node].get('type'):
                edge_list = get_family_edge(self.document_dict[self.reference_dict[node]])
                for e in edge_list:
                    self.graph.add_edge(e[0], e[1])

    def get_similars(self, reference, restart=.2):
        """
        """
        similarity_list = []
        if not self.random_walk:
            self.random_walk = RandomWalk(self.graphs[self.graphs_index])

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
                    and not self.graphs[self.graphs_index].node[key].get('type') \
                    and self.graphs[self.graphs_index].node[reference].get('block_id') == self.graphs[self.graphs_index].node[key].get('block_id') \
                    and (reference - key > 3 or reference - key < -3) \
                    and self.random_walk.proximity_dict[key] > 0:
                similarity_list.append([key, self.random_walk.proximity_dict[key]])

        return similarity_list

    def find_matches(self):
        """
        parses thought all nodes, and reports the potential mathces
        """

        log("decomposing graph")
        self.graphs = list(networkx.connected_component_subgraphs(self.graph))
        print len(self.graphs)

        log("starting the random walk on first graph")
        this_graph = self.graphs[self.graphs_index]

        for node in this_graph:
            log('random_walk on node %s' % node)
            if not this_graph.node[node].get('type'):   # if node is a reference
                similars_list = self.get_similars(node)

                for sim in similars_list:
                    self.export_results([node, sim[0], sim[1]])  # ref1, ref2, score

            self.export_results()

    def export_results(self, message_list=None):
        """
        gets a list of values that stores them in a csv file with comma delimited
        """

        if DEBUG:
            log(message_list)

        if message_list:
            message = str(self.message_counter) + ','
            for msg in message_list:
                message += str(msg) + ','
            message += '\N,\N\n'

            self.export_message += message
            self.message_counter += 1

        if self.message_counter % 2 == 1 or not message_list:
            with open(FILE_NAME % MAX_REFERENCES, 'a') as csv_file:
                csv_file.write(self.export_message)
            self.export_message = ''


def main():

    entity_resolution = EntityResolution()
    log("loading data")
    entity_resolution.load_dictionary(False, MAX_REFERENCES)
    log("constructing graph")
    entity_resolution.load_graph()
    entity_resolution.find_matches()

    # print graphs

    # print entity_resolution.graph.connected_components()


if __name__ == "__main__":
    main()


