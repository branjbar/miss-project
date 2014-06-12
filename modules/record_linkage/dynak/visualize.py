__author__ = 'Bijan'


import matplotlib
from modules.basic_modules import basic


matplotlib.use('TkAgg')

import pylab as PL
import networkx as NX
network = NX.Graph()

db = basic.do_connect()
query1 = """
            SELECT ref1, (select reference_ids from all_documents WHERE id = (
            SELECT register_id FROM links_based.all_persons_new WHERE id = ref1)),
            ref2, (select reference_ids from all_documents where id = (
            SELECT register_id FROM links_based.all_persons_new where id = ref2))
            from miss_matches order by score desc limit 1000
        """

ref_list = []
cur = basic.run_query(db, query1)
for c in cur.fetchall():
    # print c[0], c[1].split(','),c[2], c[3].split(',')
    for ref in c[1].split(','):
        network.add_edge(str(c[0]),str(ref), weight=1)

    for ref in c[3].split(','):
        network.add_edge(str(c[2]),str(ref), weight=1)

    network.add_edge(str(c[0]),str(c[2]), weight=100)

# PL.cla()
# positions = NX.spring_layout(network)
# NX.draw(network, pos=positions)
NX.write_gml(network, "graph_for_gephi.gml")
# PL.show()
# print ref_list
