"""
Here we do the hashing and update, search the """

import solr
from modules.basic_modules.basic import log
NOTARY_OFFSET_old = 4000000
NOTARY_OFFSET = 30000000


def generate_features(r1, r2):
    if r1[0] and r1[-1] and r2[0] and r2[-1]:
        if not r1[0] == '*' and not r2[0] == '*':
            r1 = [r1[0], r1[-1]]
            r2 = [r2[0], r2[-1]]
            feature = sorted(['_'.join(r1), '_'.join(r2)])
        else:
            feature = ['*']


        return '_'.join(feature)
    else:
        return 'ERROR'

class SolrQuery():
    def __init__(self):
        """
        initializes the Solr connection
        :return:
        """
        self.s = solr.SolrConnection('http://localhost:8983/solr')
        self.commit_counter = 0
        self.commit_number = 0
        self.current_document_id = 0
        self.place = ''
        self.date = ''
        self.register_type = ''

    def search(self, features_list, filter_query):

        if features_list:
            query = 'features: ' + features_list + '~'

        filter_query = filter_query.split(' -')
        # log(query)
        query_results = self.s.query(query, fq=filter_query, rows=60, highlight=True, facet='true',
                                     facet_field=['features_ss', 'location_s', 'cat'],
                                     facet_range='date_dt',
                                     facet_range_start='1700-00-00T00:00:00Z',
                                     facet_range_end='1900-00-00T00:00:00Z',
                                     facet_range_gap='+10YEAR',
                                     fields="features, id, score")

        return query_results