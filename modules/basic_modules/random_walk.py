__author__ = 'Bijan'

import networkx as nx
import random
import matplotlib
matplotlib.use('TkAgg')
import pylab

# TODO: Replace the current random walk with the Java code that Hossein gave me.

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
    n = 30  # 30 nodes
    m = 40  # 40 edges

    graph = nx.gnm_random_graph(n,m)
    nx.draw(graph)
    proximity = get_proximity(graph, 0, 40, .1)
    print proximity
    pylab.cla()

    color = []
    proximity[0] = max(proximity.values())+1
    for node in graph.nodes():
        color.append(proximity.get(node,0))

    positions = nx.circular_layout(graph)
    nx.draw(graph, pos=positions, node_color=color)
    pylab.show()


if __name__ == "__main__":
    main()
