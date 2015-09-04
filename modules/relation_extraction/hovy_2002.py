from modules.solr_search.solr_query import SolrQuery
from modules.basic_modules.basic import run_query, log, write_list_to_csv
from modules.NERD.dict_based_nerd import Nerd

__author__ = 'bijan'
"""
Here we implement the work of Ravichandran and Hovy presented in "Learning Surface Text Patterns for Question Answering System"
"""


my_solr = SolrQuery()
search_results = my_solr.search('*','cat:death or cat:birth or cat:marriage')

for result in search_results.results:
    couples_list = result['features']
    for couple in couples_list:

        my_solr.search('*','cat:death or cat:birth or cat:marriage')
