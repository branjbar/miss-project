__author__ = 'Bijan'

from modules.basic_modules import basic
import networkx as nx
import random
import matplotlib
matplotlib.use('TkAgg')
import pylab
import math
import copy

# TODO: Replace the current random walk with the Java code that Hossein gave me.

CONVERSION_THRESHOLDS = 0.0001
CONVERSION_ITERATIONS = 10000


def l2(a, b):
    """
    finds the l2 norm between two dictionaries
    """
    result = 0
    for key in a.keys():
        result += (a[key] - b[key]) * (a[key] - b[key])

    return math.sqrt(result)


class RandomWalk():
    """
    This function computes the steady state distribution of Random Walk with Restarts (RWR):
    S^j(t+1) = (1-r)M^TS^j(t) + rX
    where M is the adjacency matrix and M is row normalized. S^j is the neighborhood profile of node j.
    Component S^j_i is proportional to the frequency of visits to node in the RWR from node j.
    X is the initial state of the random walk. When S^j(t) converges, we'll get the final neighborhood profile.

    Reference: Petko Bogdanov and Ambuj Singh, "Function Prediction Using Neighborhood Patterns"

    """
    def __init__(self, graph):
        """ (graph)
        initializes the RandomWalk class
        graph: a networkx graph
        """

        self.graph = graph   # a graph in networkx structure
        self.n = self.graph.number_of_nodes()  # size of graph
        self.x_initial = {}
        self.proximity_dict = {}  # stores the final results with respect to starting nodes
        self.start_nodes = []  # stores list of starting nodes for the random walk

    def generate_x_initial(self, start_nodes):
        """
        generates the x_initial w.r.t. the list of starting nodes
        """
        self.start_nodes = start_nodes
        self.x_initial = {node: 0 for node in self.graph.nodes()}
        for node in start_nodes:
            self.x_initial[node] = 1.0 / len(start_nodes)



    def run_uniform(self, restart=.3):
        """ (list, int) --> (list)

        x_initial: initial state of random walk. Usually all of its elements are zero except the target node(s).
                   if we put every node 1/n, then we'll get a page rank.

        """

        x_old = copy.deepcopy(self.x_initial)  # known as S(t) in the paper
        diff = 1.0
        it = 0

        while diff > CONVERSION_THRESHOLDS and it < CONVERSION_ITERATIONS:
            if it and not it % 1000:
                basic.log("RWR algorithm is in iteration %d and steady state error is %.3f" % (it, diff))

            x = {node: 0 for node in self.graph.nodes()}  # initializing a zero vector

            for edge in self.graph.edges():
                w_target = 1.0 / self.graph.degree(edge[1])  # normalizing the weights
                w_source = 1.0 / self.graph.degree(edge[0])  # normalizing the weights

                x[edge[0]] += (1.0 - restart) * w_target * x_old[edge[1]]
                x[edge[1]] += (1.0 - restart) * w_source * x_old[edge[0]]

            for node in self.graph.nodes():
                x[node] += restart * self.x_initial[node]

            diff = l2(x, x_old)
            it += 1
            x_old = copy.deepcopy(x)

        self.proximity_dict = copy.deepcopy(x_old)


def main():
    n = 20  # 30 nodes
    m = 40  # 40 edges
    from modules.basic_modules.basic import log
    log('making the graph')
    graph = nx.gnm_random_graph(n,m)
    # log('making the adjcency matrix')
    # A = nx.adjacency_matrix(graph)

    rw = RandomWalk(graph)
    rw.generate_x_initial([1,2])
    rw.run_uniform(.3)


    #
    # print basic.get_top_k_heap_search(color, 4)
    # print basic.get_top_k_linear_search(color, 4)

    color = [rw.proximity_dict[node] for node in rw.graph.nodes()]

    pylab.cla()
    positions = nx.circular_layout(graph)
    nx.draw(graph, pos=positions, node_color=color)
    pylab.show()


if __name__ == "__main__":
    main()
