"""
    This code builds a huge graph in which each node is an individual and edges are either because of family relations
     or blocking keys.

At the end the exported csv file can be imported in mysql using:
    LOAD DATA INFILE '/Users/Bijan/sandbox/Eclipse_Projects/linkPy/data/matching_kdd/matches_random_walk_100.csv'
    INTO TABLE miss_matches_random_walk FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';


"""
import matplotlib
matplotlib.use('TkAgg')
import pylab
import networkx
import operator
import time
import math
from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.dynak.visualize import get_family_edge
from modules.basic_modules.random_walk import get_proximity
import os

FILE_NAME = "../../../data/matching_kdd/matches_random_walk_%d.csv"


def load_graph(from_file=False, limit=1000):
    """
        loads a graph either from file or directly from sql
        block_dict = {block_id: [ref1_id, ref2_id, ...]}
        document_dict = {document_id: [ref1_id, ref2_id, ...]}
    """
    if not from_file:

        log("start gathering blocks and documents")

        block_dict = {}
        document_dict = {}
        reference_dict = {}
        # let's keep it as light as possible
        block_query = """
                        SELECT id, block_id, register_id
                        FROM links_based.all_persons_new
                        LIMIT %d
                      """ % limit
        db = basic.do_connect()
        cur = basic.run_query(block_query)

        for c in cur.fetchall():
            ref_id = c[0]
            block_id = c[1]
            register_id = c[2]
            reference_dict[ref_id] = register_id
            if block_id != 1888:
                block_dict[block_id] = block_dict.get(block_id,[]) + [ref_id]
            document_dict[register_id] = document_dict.get(register_id, []) + [ref_id]

        log("start building the graph based on blocks")
        G = networkx.Graph()

        # add block edges first
        for block_id in block_dict.keys():
            ref_list = block_dict[block_id]
            if len(ref_list) < 30:  # to avoid huge graphs for now, just limit it to blocks with size less than 30
                for ref1 in ref_list:
                    for ref2 in ref_list:
                        if ref2 > ref1:
                            G.add_node(ref1, block_id=block_id)
                            G.add_node(ref2, block_id=block_id)
                            G.add_edge(ref1, ref2)

        log("start adding the family relations")

        for node in G.nodes():
            edge_list = get_family_edge(document_dict[reference_dict[node]])
            for e in edge_list:
                G.add_edge(e[0], e[1])

    return G


    # log("Visualizing the graph")

    # print networkx.communicability_exp(G)
    # pylab.cla()
    # positions = networkx.circular_layout(G)
    # networkx.draw(G, pos=positions)
    # NX.write_gml(network, "graph_for_gephi.gml")
    # pylab.show()

def get_similarity_random_walk(graph, max_iteration=100, reset_c=.5):
    """ (graph) --> (list)
        for a given graph, return a list of feasible matches
    """
    try:
        os.remove(FILE_NAME % max_iteration)  # to be sure data will not be appended to a non-empty file
    except:
        pass


    log("walking randomly")
    now = time.time()
    count = 1
    csv_text = ''
    for ref1 in graph.nodes():
        block_id = graph.node[ref1].get('block_id')
        if block_id:
            proximity = get_proximity(graph, ref1, max_iteration, reset_c)
            proximity = sorted(proximity.iteritems(), key=operator.itemgetter(1), reverse=True)  # sorting dict

            for link in proximity:
                if graph.node[link[0]].get('block_id') == block_id \
                        and math.fabs(link[0] - ref1) > 3: # latter is to avoid father_child match
                    ref2 = link[0]
                    score = link[1]
                    # print count, ref1, '--', link[0], '(', link[1], ')'
                    count += 1
                    csv_text += str(count) + ',' + str(ref1) + ',' + str(ref2) + ',' + str(score) +  '\n'
                    if not count % 10000:
                        log(count)
                        with open(FILE_NAME % max_iteration, "a") as my_file:
                            my_file.write(csv_text)
                        csv_text = ''

    with open(FILE_NAME % max_iteration, "a") as my_file:
        my_file.write(csv_text)
    csv_text = ''

    log("elapsed time for %d nodes (i.e., %d matches) is %s" % (len(graph.nodes()), count, str(time.time() - now) ))


def main():

    graph = load_graph(from_file=False, limit=6000000)
    get_similarity_random_walk(graph, max_iteration=100, reset_c=.5)

if __name__ == "__main__":
    main()


