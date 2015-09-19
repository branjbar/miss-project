from modules.solr_search.hashing import generate_features

__author__ = 'bijan'

from modules.basic_modules.basic import string_compare
from modules.family_network.treeStructure import TreeStructure
from modules.basic_modules.myOrm import Document
from modules.solr_search.solr_query import SolrQuery

my_hash = SolrQuery()


def recursive_search(search_results, search_term_list):
    """
    receives the search results and extracts search terms from them (i.e., couple names),
    then retrieves information for all search results.

    :param search_results: a list of solr search results
    :param search_term_list: a list of search terms (i.e., couple names) that have been already used.
    """
    solr_results_list = []

    # append new search terms to the search_term_list
    for doc_id in search_results.keys():
        doc = Document()
        doc.set_id(doc_id)
        if doc.get_couples():
            for couple in doc.get_couples():
                name1 = couple[0]
                name2 = couple[1]
                if len(name1) > 2 and len(name2) > 2:
                    search_term = generate_features(name1.split(), name2.split())
                    if search_term not in search_term_list:
                        search_term_list.append(search_term)
                        solr_results_list.append(my_hash.search(search_term, ''))

    # retrieve all solr_results for search terms
    for solr_result in solr_results_list:
        if solr_result:
            for result in solr_result.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

    return search_term_list, search_results


def get_family_from_solr(search_term_list, depth_level=1):
    """
    gets a search_term_list and a depth_level and returns are the related documents

    :param search_term_list: the terms that we search for
    :param depth_level: the depth of family network
    """
    search_results = {}
    for search_term in search_term_list:
        search_term = ' '.join(search_term.split('_'))
        search_term = search_term.replace('&', '').replace('-', '').replace('  ', ' ').replace('?', '').title()
        ref1 = ' '.join(search_term.split()[:2])
        ref2 = ' '.join(search_term.split()[-2:])

        search_term = generate_features(ref1.split(), ref2.split())
        solr_results_1 = my_hash.search(search_term, '')

        if solr_results_1:
            for result in solr_results_1.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

    new_search_term_list = [search_term]
    if depth_level:
        for i in xrange(depth_level - 1):
            new_search_term_list, search_results = recursive_search(search_results, new_search_term_list)

    return search_results


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


if __name__ == '__main__':
    # generating family netowrks using facet information
    couple_name = 'Cornelia Gommeren - Jacobus Aerts'
    print get_family_network(get_family_from_solr([],couple_name)).get_edge_list()