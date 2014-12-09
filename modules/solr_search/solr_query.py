"""
Here we do the hashing and update, search the """

import solr
from modules.basic_modules.basic import log

NOTARY_OFFSET_old = 4000000
NOTARY_OFFSET = 30000000


def generate_features(r1, r2):
    if r1[0] and r1[-1] and r2[0] and r2[-1]:
        r1 = [r1[0], r1[-1]]
        r2 = [r2[0], r2[-1]]
        if not r1[0] == '*' and not r2[0] == '*':
            feature = sorted(['_'.join(r1), '_'.join(r2)])
            return '_'.join(feature)

        else:
            if r1[0] != '*':
                return '*' + '_'.join(r1) + '*'
            if r1[0] != '*':
                return '*' + '_'.join(r2) + '*'

            # in case both references are *
            return '*'
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

    def get_support(self, r1, r2, cats):
        index_key = generate_features(r1.split(), r2.split())
        solr_results_r1r2 = self.search(index_key, cats)
        ref1_alternatives = []
        ref2_alternatives = []
        documents_list = []
        name_alternatives = []

        ####
        for r in solr_results_r1r2.highlighting.iteritems():
            refs = r[1]['features'][0].replace('<em>', '').replace('</em>', '').split('_')
            documents_list.append({'doc': r[0], 'ref': refs})

            # get name alternatives
            if not '_'.join(refs[:2]) in ref1_alternatives:
                ref1_alternatives.append('_'.join(refs[:2]))
            if not '_'.join(refs[2:]) in ref2_alternatives:
                ref2_alternatives.append('_'.join(refs[2:]))

        sup_r1 = 0
        for r1 in ref1_alternatives:
            index_key = generate_features(r1.split('_'), ['*'])
            solr_results_r1 = self.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
            sup_r1 += solr_results_r1.numFound

        sup_r2 = 0
        for r2 in ref2_alternatives:
            index_key = generate_features(r2.split('_'), ['*'])
            solr_results_r2 = self.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
            sup_r2 += solr_results_r2.numFound

        sup_r1r2 = solr_results_r1r2.numFound

        return {'support': [sup_r1r2, sup_r1, sup_r2], 'refs': [r1, r2]}