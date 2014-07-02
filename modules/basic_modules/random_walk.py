__author__ = 'Bijan'

import networkx as nx
import random
import matplotlib
matplotlib.use('TkAgg')
import pylab
import math

# TODO: Replace the current random walk with the Java code that Hossein gave me.


class RWalk():
    """
    A class to implement the random walk in a graph.
    """

    def __init__(self):
        self.am = []  # adjacency matrix
        self.w = []  # public double[] w;
        self.n = 0  # number of robots

        self.conversion_threshold = 0.0000000000001  # conversion threshold

        self.conversion_iterations = 1000000000  # conversion iterations

        self.volume = None  # public double[] volume = null;

    # public RWalk(String file) throws IOException{
    #     BufferedReader fr = new BufferedReader(new FileReader(file));
    #     HashMap<String,Double> hm =new HashMap<String,Double>();
    #     int maxid =-1;
    #     String line=null;
    #     while((line=fr.readLine())!=null){
    #         int id1=Integer.parseInt(line.split("\t")[0]);
    #         int id2=Integer.parseInt(line.split("\t")[1]);
    #         Double w= 1.0;
    #         if(line.split("\t").length==3)
    #             w=Double.parseDouble(line.split("\t")[2]);
    #         if(id1>maxid) maxid=id1;
    #         if(id2>maxid) maxid=id2;
    #         hm.put(id1 + "\t" + id2, w);
    #         hm.put(id2 + "\t" + id1, w);
    #     }
    #     am=new int[hm.size()][2];
    #     w = new double[hm.size()];
    #     int counter = 0;
    #     for(String k:hm.keySet()){
    #         am[counter][0]=Integer.parseInt(k.split("\t")[0]);
    #         am[counter][1]=Integer.parseInt(k.split("\t")[1]);
    #         w[counter++]=hm.get(k);
    #     }
    #     fr.close();
    #     n = maxid+1;
    #     colNormalize();
    # }

    def __init__(self, pam, pw, pn):
        self.am = pam.copy()
        self.w = pw.copy()
        self.n = pn.copy()
        self.colNormalize()

    def numNodes(self):
        return self.n

    def colNormalize(self):

        self.volume = [] * self.n

        for i in xrange(len(self.am)):
            self.volume[self.am[i][1]] += self.w[i]

        for i in xrange(len(self.w)):
            self.w[i] = self.w[i]/self.volume[self.am[i][1]]

    def runUniform(self, restart):
        x = [0] * self.n
        xold = [1.0/self.n] * self.n
        diff = 1.0
        it = 0

        while diff> self.conversion_threshold and it < self.conversion_iterations:
            for i in xrange(len(self.am)):
                x[self.am[i][0]] += (1.0-restart) * self.w[i] * xold[self.am[i][1]]

            for i in xrange(len(self.am)):
                x[i] += restart/self.n


            diff = self.l2(x, xold);
            it += 1
            xold = x.copy()

            x  = [0] * self.n

        return xold
    #
    #
    # public double[] runNonUniform(double restart, int index){
    #     int[] indices= new int[1];
    #     indices[0]=index;
    #     return runNonUniform(restart,indices);
    # }

    def runNonUniform(self, restart, indices):

        x  = [0] * self.n
        xold = [0] * self.n
        diff = 1.0
        it = 0

        for i in xrange(len(indices)):
            xold[indices[i]] = 1.0/len(indices)

        while diff> self.conversion_threshold and it < self.conversion_iterations:
            for i in xrange(len(self.am)):
                x[self.am[i][0]] += (1-restart) * self.w[i] * xold[self.am[i][1]]

            for i in xrange(len(self.am)):
                x[i] += restart/len(indices)


            diff = self.l2(x, xold);
            it += 1
            xold = x.copy()


            x = [0] * self.n

        norm = 0.0
        for i in xold:
            norm += i;
        if math.abs(norm - 1.0) > 0.0000000001:
            print "non normalized vector" + norm
        return xold

    def l2(self, a, b):
        result = 0
        for i in xrange(len(a)):
            result += (a[i]-b[i])*(a[i]-b[i])

        return math.sqrt(result)

    @staticmethod
    def print_vector(a, v=None):
        for i in xrange(len(a)):
            if not v:
                print i + "\t" + str(a[i]) + "\n"
            else:
                print i + "\t" + str(a[i]) + "\t" + str(v[i]) + "\t"  + str(a[i] * 1.0/v[i]) + "\n"


def main():
    file = "test.csv"
    restart = .5
    uniform = False
    rnode = -1

    rw = RWalk()
    x = None

    if uniform:
        x = rw.runUniform(restart)
    else:
        rnodes = []
        rnodes[0] = rnode
        x = rw.runNonUniform(restart, rnodes)

        rw.print_vector(x,rw.volume)


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
    n = 25000  # 30 nodes
    m = 40000  # 40 edges
    from modules.basic_modules.basic import log
    log('making the graph')
    graph = nx.gnm_random_graph(n,m)
    # log('making the adjcency matrix')
    # A = nx.adjacency_matrix(graph)
    log('Accessing an element')
    print graph.neighbors(graph.nodes()[1])

    # print A


    # nx.draw(graph)

    # proximity = get_proximity(graph, 0, 40, .1)
    # print proximity
    #
    # pylab.cla()
    # color = []
    # proximity[0] = max(proximity.values())+1
    # for node in graph.nodes():
    #     color.append(proximity.get(node,0))
    #
    # positions = nx.circular_layout(graph)
    # nx.draw(graph, pos=positions, node_color=color)
    # pylab.show()


if __name__ == "__main__":
    main()
