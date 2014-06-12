__author__ = 'Bijan'


import matplotlib
from modules.basic_modules import basic


def get_family_edge(ref_list):
    """ (list) --> (list)
        gets a list of references in the same document and depending of the lenght of list
        generates the family edges
    """

    edge_list = []

    if len(ref_list) == 3:
        # birth
        edge_list.append([ref_list[0], ref_list[1],'father_child'])  #child-father
        edge_list.append([ref_list[0], ref_list[2],'mother_child'])  #child-mother
        edge_list.append([ref_list[1], ref_list[2],'partner'])  #father-mother

    if len(ref_list) == 4:
        # death
        edge_list.append([ref_list[0], ref_list[1],'father_child'])  #deceased-father
        edge_list.append([ref_list[0], ref_list[2],'mother_child'])  #deceased-mother
        edge_list.append([ref_list[1], ref_list[2],'partner'])  #father-mother
        edge_list.append([ref_list[0], ref_list[3],'partner'])  #deceased-partner

    if len(ref_list) == 6:
        # marriage
        edge_list.append([ref_list[0], ref_list[1],'partner'])  #groom-bride
        edge_list.append([ref_list[0], ref_list[2],'father_child'])  #groom-father
        edge_list.append([ref_list[0], ref_list[3],'mother_child'])  #groom-mother
        edge_list.append([ref_list[2], ref_list[3],'partner'])  #groomfather-groommother
        edge_list.append([ref_list[1], ref_list[4],'father_child'])  #bride-father
        edge_list.append([ref_list[1], ref_list[5],'mother_child'])  #bride-mother
        edge_list.append([ref_list[4], ref_list[5],'partner'])  #bridefather-bridemother

    return edge_list



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
            from miss_matches order by score desc limit 10000
        """

ref_list = []
cur = basic.run_query(db, query1)
for c in cur.fetchall():
    edge_list = get_family_edge(c[1].split(','))
    for e in edge_list:
        network.add_edge(str(e[0]),str(e[1]), weight=1, type=e[2])

    edge_list = get_family_edge(c[3].split(','))
    for e in edge_list:
        network.add_edge(str(e[0]),str(e[1]), weight=1, type=e[2])

    network.add_edge(str(c[0]),str(c[2]), weight=100)

# PL.cla()
# positions = NX.spring_layout(network)
# NX.draw(network, pos=positions)
NX.write_gml(network, "graph_for_gephi.gml")
# PL.show()
# print ref_list

