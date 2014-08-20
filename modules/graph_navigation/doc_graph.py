import networkx
from modules.basic_modules.basic import run_query, log

__author__ = 'bijan'
"""
here we construct the document graph and study that
e.g., how blocks can change the number of connected components.
"""


class DocGraph():
    def __init__(self):
        self.block_dict = {}  # block_dict = {block_id: size}
        self.document_dict = {}  # document_dict = {document_id: [block_id1, block_id2, ...]}
        self.reference_dict = {}  # reference_dict = {ref_id: document_id}

        self.graph = networkx.Graph()  # a graph. nodes: refs and blocks, edges: family relations and block membership

    def collect_data(self):
        """
        collect required data for constructing the graph
        :return:
        """

        query = "SELECT id, block_id, register_id FROM links_based.all_persons_new limit 1000000000"

        cur = run_query(query)

        for c in cur:
            ref_id = c[0]
            block_key = c[1]
            doc_id = c[2]

            self.block_dict[block_key] = self.block_dict.get(block_key, []) + [doc_id]
            self.document_dict[doc_id] = self.document_dict.get(doc_id, []) + [block_key]


    def construct_graph(self, threshold):
        """
        construct the graph from collected data
        :return:
        """
        for doc_id in self.document_dict.keys():
            self.graph.add_node(doc_id, node_type='d')

        for block_key in self.block_dict.keys():
            if len(self.block_dict[block_key]) < threshold:
                self.graph.add_node(block_key, node_type='b')

                for doc_id in self.block_dict[block_key]:
                    self.graph.add_edge(block_key, doc_id)




    def get_number_of_connected_components(self):

        return networkx.number_connected_components(self.graph)


if __name__ == '__main__':
    my_graph = DocGraph()
    log("collecting data")
    my_graph.collect_data()
    for thresh in xrange(100):
        my_graph.graph = networkx.Graph()
        my_graph.construct_graph(thresh)
        print str(thresh) + ', ' + str(my_graph.get_number_of_connected_components())

