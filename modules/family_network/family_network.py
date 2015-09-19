__author__ = 'bijan'

from modules.basic_modules.basic import string_compare
from modules.family_network.treeStructure import TreeStructure
from modules.basic_modules.myOrm import Document


def get_family_network(search_term_list, solr_search_results):
    """
    receives the information retrieved by solr and returns a nice family tree
    """
    tree = TreeStructure()
    if solr_search_results:

        for doc_id in solr_search_results.keys():
            doc = Document()
            doc.set_id(doc_id)
            new_data = doc.get_relatives(solr_search_results[doc_id], [])
            for leaf in new_data['leaves']:
                name1 = leaf.node1['name']
                name2 = leaf.node2['name']
                for search_term in search_term_list:
                    if string_compare(name1 + ' ' + name2, search_term.replace('_', ' '), 'LEV') < 4 or string_compare(
                                            name2 + ' ' + name1, search_term.replace('_', ' '), 'LEV') < 4:
                        leaf.color = "Coral"

                tree.add_leaf(leaf)
            for branch in new_data['branches']:
                tree.add_branch(branch)

    tree.update()
    return tree