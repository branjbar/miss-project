__author__ = 'Bijan'

import networkx as nx
import random
import matplotlib
matplotlib.use('TkAgg')
import pylab
import math

# TODO: Replace the current random walk with the Java code that Hossein gave me.

CONVERSION_THRESHOLDS = 0.0000000000001
CONVERSION_ITERATIONS = 10000


def l2(a, b):
    result = 0
    for i in xrange(len(a)):
        result += (a[i] - b[i]) * (a[i] - b[i])

    return math.sqrt(result)


class RandomWalk():
    def __init__(self, graph):
        """
        initializes the RandomWalk class by a graph
        """

        self.graph = graph   # a graph in networkx structure
        self.n = self.graph.number_of_nodes()  # size of graph

    def run_uniform(self, restart):
        """ (int) --> (list)

        """
        x = [0] * self.n
        x_old = [1.0/self.n] * self.n
        diff = 1.0
        it = 0
        while diff > CONVERSION_THRESHOLDS and it < CONVERSION_ITERATIONS:

            for edge in self.graph.edges():
                x[edge[0]] += (1.0 - restart) * (1.0 / self.graph.degree(edge[1])) * x_old[edge[1]]
                # x[self.am[i][0]] += (1.0-restart) * self.w[i] * xold[self.am[i][1]]

            for i in xrange(self.n):
                x[i] += restart/self.n

            diff = l2(x, x_old)
            it += 1
            x_old = x[:]

        return x_old


# one shot random_walk
def single_random_step(graph, node_s, visited=[]):

    next_node = None
    neighbors = graph.neighbors(node_s)
    feasible_neighbors = list(set(neighbors) - set(visited))  # excluding already visited nodes
    if feasible_neighbors:
        next_node = random.choice(feasible_neighbors)

    return next_node


def random_walk(graph, node_s, restart_c=0.1):
    """
        starts from node_s and moves ahead until it decides to restart,
        at this point it exports the one shot proximity dict
    """
    next_node = single_random_step(graph, node_s)
    if not next_node and not next_node == 0:
        return [node_s]  # just in case the node is isolated

    visited = [node_s, next_node]
    while random.random() >= restart_c:
        next_node = single_random_step(graph, visited[-1], visited)

        if not next_node:
            return visited

        visited.append(next_node)

    return visited


# proximity detection
def get_proximity(graph, node_s, max_iteration, restart_c=.5):
    """ (graph, node, float) --> dict
        returns the proximity vector that contains the closeness of each node to node_s
    """

    proximity = {}
    counter = 0  # counts number of visited nodes
    if restart_c == 0:
        restart_c = 0.05  # just to avoid getting stuck in a never ending loop

    visitor_list = []
    counter = 0
    while counter < max_iteration :
        visitor_list.append(random_walk(graph, node_s, restart_c))

        if not len(visitor_list[-1]):
            counter = max_iteration  # in case of having an isolated node, we'll get a null vector immediately

        counter += len(visitor_list[-1])

    for visit in visitor_list:
        distance = 0  # distance to node_s
        for node in visit[1:]:  # to skip node_s which is always the first in array
            distance += 1
            proximity[node] = 1.0 / distance + proximity.get(node,0)

    return proximity


def main():
    n = 40  # 30 nodes
    m = 40  # 40 edges
    from modules.basic_modules.basic import log
    log('making the graph')
    graph = nx.gnm_random_graph(n,m)
    # log('making the adjcency matrix')
    # A = nx.adjacency_matrix(graph)
    log('Accessing an element')
    rw = RandomWalk(graph)
    color = rw.run_uniform(.4)
    print color
    # print graph.neighbors(graph.nodes()[1])

    # print A


    # nx.draw(graph)

    # proximity = get_proximity(graph, 0, 40, .1)
    # print proximity
    #
    pylab.cla()
    # color = []
    # proximity[0] = max(proximity.values())+1
    # for node in graph.nodes():
    #     color.append(proximity.get(node,0))
    #
    positions = nx.circular_layout(graph)
    nx.draw(graph, pos=positions, node_color=color)
    pylab.show()


if __name__ == "__main__":
    main()
