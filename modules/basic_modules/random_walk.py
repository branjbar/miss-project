__author__ = 'Bijan'

from modules.basic_modules import basic
import networkx as nx
import random
import matplotlib

matplotlib.use('TkAgg')
import pylab
import math
import copy

CONVERSION_THRESHOLDS = 0.000000001
CONVERSION_ITERATIONS = 100
LOCAL_NEIGHBORHOOD = 5


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

        self.graph = graph  # a graph in networkx structure
        self.n = self.graph.number_of_nodes()  # size of graph
        self.x_initial = {}
        self.proximity_dict = {}  # stores the final results with respect to starting nodes
        self.start_nodes = []  # stores list of starting nodes for the random walk
        self.exclude_nodes = []  # list of nodes which should be excluded from random walk
        self.zero_dict = {}  # to save time, this dict is stored to increase efficiency
        self.w = {}  # the dictionary of neighbors

        self.important_nodes = []  # contains a list of important nodes close to start node, which should be explored
        self.important_edges = []  # contains a list of important edges close to start node, which should be explored

    def generate_x_initial(self, start_nodes):
        """
        generates the x_initial w.r.t. the list of starting nodes
        """
        # TODO: Implement the exclude nodes to the non-intelligent random walk

        self.zero_dict = {node: 0 for node in
                          self.graph.nodes()}  # to save time, this dict is stored to increase efficiency

        self.start_nodes = start_nodes
        self.w = {node: 1.0 / self.graph.degree(node) for node in self.graph.nodes()}

        self.x_initial = {node: 0 for node in self.graph.nodes()}
        for node in start_nodes:
            self.x_initial[node] = 1.0 / len(start_nodes)

    def run_uniform(self, start_nodes, restart=.3):
        """ (int) --> (list)
        runs a uniform random walk

        """

        self.generate_x_initial(start_nodes)

        x_old = self.x_initial.copy()  # known as S(t) in the paper
        diff = 1.0
        it = 0

        while diff > CONVERSION_THRESHOLDS and it < CONVERSION_ITERATIONS:
            if it and not it % 1000:
                basic.log("RWR algorithm is in iteration %d and steady state error is %.3f" % (it, diff))

            x = self.zero_dict.copy()  # initializing a zero vector

            for edge in self.graph.edges():
                x[edge[0]] += (1.0 - restart) * self.w[edge[1]] * x_old[edge[1]]
                x[edge[1]] += (1.0 - restart) * self.w[edge[0]] * x_old[edge[0]]

            for node in self.graph.nodes():
                x[node] += restart * self.x_initial[node]

            diff = l2(x, x_old)
            it += 1
            x_old = x.copy()

        self.proximity_dict = x_old.copy()

    def get_important_nodes(self, k=LOCAL_NEIGHBORHOOD):
        """
        returns a list of neighbors up to kth neighbor
        """
        neighbors_list = [set(self.start_nodes)]

        for l in range(k):
            neighbors_list.append(set((neighbor for n in neighbors_list[-1] for neighbor in self.graph[n])))

        neighbors_set = set([])
        for neighbors in neighbors_list:
            neighbors_set = neighbors_set.union(neighbors)

        # TODO: now excluded nodes is just a node, adapt it to a list.
        neighbors_set.discard(self.exclude_nodes)
        self.important_nodes = list(neighbors_set)

    def get_important_edges(self):
        """
        based on important nodes, figures out a list of important edges
        """
        self.important_edges = self.graph.edges(self.important_nodes)

    def generate_intelligent_x_initial(self, start_nodes):
        """
            generates the x_initial w.r.t. the list of starting nodes
            """

        self.start_nodes = start_nodes

        self.get_important_nodes()
        self.get_important_edges()

        self.zero_dict = {node: 0 for node in
                          self.important_nodes}  # to save time, this dict is stored to increase efficiency

        for node in self.important_nodes:
             # degree of node among important nodes
            local_degree = len(set(self.important_nodes).intersection(self.graph[node]))
            if local_degree > 0:
                self.w[node] = 1.0 / local_degree
            else:
                self.w[node] = 0.00001

        self.x_initial = {node: 0 for node in self.important_nodes}
        for node in start_nodes:
            self.x_initial[node] = 1.0 / len(start_nodes)

    def run_intelligent_uniform(self, start_nodes, restart=.3, exclude_nodes=[]):
        """ (int) --> (list)

        x_initial: initial state of random walk. Usually all of its elements are zero except the target node(s).
                   if we put every node 1/n, then we'll get a page rank.

        """

        self.exclude_nodes = exclude_nodes
        self.generate_intelligent_x_initial(start_nodes)
        x_old = self.x_initial.copy()  # known as S(t) in the paper

        diff = 1.0
        it = 0

        while diff > CONVERSION_THRESHOLDS and it < CONVERSION_ITERATIONS:
            if it and not it % 1000:
                basic.log("RWR algorithm is in iteration %d and steady state error is %.3f" % (it, diff))

            x = self.zero_dict.copy()  # initializing a zero vector

            for edge in self.important_edges:
                if x.get(edge[0], -1) != -1 and x.get(edge[1], -1) != -1:
                    x[edge[0]] += (1.0 - restart) * self.w[edge[1]] * x_old[edge[1]]
                    x[edge[1]] += (1.0 - restart) * self.w[edge[0]] * x_old[edge[0]]

            for node in self.important_nodes:
                x[node] += restart * self.x_initial[node]

            diff = l2(x, x_old)
            it += 1
            x_old = x.copy()
        # TODO: normalize the proximity vector locally
        self.proximity_dict = x_old.copy()


def main():
    n = 20  # 30 nodes
    m = 40  # 40 edges
    from modules.basic_modules.basic import log

    log('making the graph')
    graph = nx.gnm_random_graph(n, m)
    # log('making the adjcency matrix')
    # A = nx.adjacency_matrix(graph)

    rw = RandomWalk(graph)
    rw.run_uniform([0], .2)
    color_1 = [rw.proximity_dict[node] for node in rw.graph.nodes()]
    labels = {node: "%s)%.3f" % (node, rw.proximity_dict[node]) for node in rw.graph.nodes()}
    pylab.cla()
    positions = nx.circular_layout(graph)
    nx.draw(graph, pos=positions, node_color=color_1, labels=labels)
    pylab.show()



if __name__ == "__main__":
    main()
